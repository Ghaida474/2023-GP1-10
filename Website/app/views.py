from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .forms import Loginform  # Import your login form
from .models import Admin, FacultyStaff, Kaibuemployee
from django.conf import settings
from .forms import ForgetPasswordForm
from django.conf import settings
from django.core.mail import send_mail
import random
import string
#from .models import PasswordResetTable
import smtplib
import ssl

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import emailcheckform
import certifi
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta

def index(request):
    # This view renders the 'index.html' for the main app.
    return render(request, 'auth/index.html')

def forgot_password(request):
    return redirect('app:index')
    # Your code here


def login_view(request):

    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the appropriate page based on the user's type
                if role == 'facultyandstaff' and user.position == 'Collage faculty' or user.position == 'Collage staff' and user.is_buhead == False:
                    return redirect('faculty_staff_account:faculty_staff_home')
                            
                elif role =='kaistaff' and user.position == 'KAI staff':
                    return redirect('kaistaff_account:kaistaff_home')
                            
                elif role =='Hkai' and  user.position == 'KAI head':
                    return redirect('kai_account:kai_home')
                            
                elif  role == 'dean' and user.position == 'Dean of collage':
                    return redirect('dean_account:dean-account-home')
                            
                elif  role == 'BU' and user.is_buhead == True:
                    return redirect('business_unit_account:business_unit_home')   
                
            # Authentication failed
            messages.error(request, 'Invalid email, password or role.')
        else:
            messages.error(request, 'Form is invalid. Please check your input.')
    else: 
        form = Loginform()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.error(request, 'You have been logged out successfully.')
    return redirect('app:login')  


def forgot_password(request):
    #form = ForgetPasswordForm()
    form = Loginform()
    return render(request, 'auth/forgot-password.html', {'form':form} )




def check_user_to_role(request, email, role):
    role = role.lower()
    user = None

    print(f"Checking role: {role} for email: {email}")

    if role in ['facultyandstaff', 'dean', 'bu']:
        try:
            user = FacultyStaff.objects.get(email=email)
        except FacultyStaff.DoesNotExist:
            print(f"No FacultyStaff found with email: {email}")
            return False

        if role == 'facultyandstaff' and user.position in ['Collage faculty', 'Collage staff'] and not user.is_buhead:
            print("Matched FacultyStaff with position 'facultyandstaff'")
            return True


    if role == 'dean' and user.position == 'Dean of collage':
            print("Matched FacultyStaff with position 'dean'")
            return True

    if role == 'bu' and user.is_buhead:
            print("Matched FacultyStaff with position 'bu'")
            return True

    elif role in ['kaistaff', 'hkai']:
        try:
            user = Kaibuemployee.objects.get(email=email)
        except Kaibuemployee.DoesNotExist:
            print(f"No Kaibuemployee found with email: {email}")
            return False

        if role == 'kaistaff' and user.position == 'KAI staff':
            print("Matched Kaibuemployee with position 'kaistaff'")
            return True

        if role == 'hkai' and user.position == 'KAI head':
            print("Matched Kaibuemployee with position 'hkai'")
            return True

    print("No matching role found")
    return False








def forgot_password_view(request):
    

    if request.method == 'POST':
        form = emailcheckform(request.POST)
        print("Form errors before validation:", form.errors)  # Debug print
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            print(email, role)

        # Call check_user_to_role and print a message based on its return value
            if check_user_to_role(request, email, role):
                print("User's credentials check")
                send_email_to_reset_password(request, email, role)
                return redirect('app:reset_password', email=email, role=role)

            else:
                print("User's credentials fail")
                messages.error(request, 'Invalid email or role')
            # Stay on the current page with the form displaying the error 
                form = emailcheckform()
                return render(request, 'auth/forgot-password.html', {'form': form})
        
    form = emailcheckform()

    return render(request, 'auth/forgot-password.html', {'form': form})


from django.utils import timezone


def send_email_to_reset_password(request, email, role):
    print("send email function entered successfully")
    print("receiver email", email)

    # Generate a 6-digit OTP
    otp = ''.join(random.choice(string.digits) for _ in range(6))
    print(otp)

    # Construct the email message
    subject = 'Password Reset OTP'
    message = 'Subject: {}\n\nYour OTP for password reset is: {}'.format(subject, otp)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Create the SSL context
    context = ssl.create_default_context(cafile=certifi.where())

    # Create connection
    connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    connection.starttls(context=context)

    # Login
    connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Send email
    connection.sendmail(email_from, recipient_list, message)

    # Close connection
    connection.quit()

    print("correctly entered the function")

    # Store OTP and the current timestamp in session
    request.session['otp'] = otp
    request.session['otp_timestamp'] = str(timezone.now())

    return HttpResponse("Password reset email sent.")

def reset_password(request, email, role):
    context = {'email': email, 'role': role}
    return render(request, 'auth/reset-password.html', context)



def reset_password_action(request, email, role):
    context = {}  # Define your context here
    if request.method == 'POST':
        # Handle POST request

        # Get the OTP, new password, and confirm password from the POST request
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Get the stored OTP and timestamp from the session
        stored_otp = request.session.get('otp')
        stored_timestamp_str = request.session.get('otp_timestamp')

        if not all([otp, new_password, confirm_password, stored_otp, stored_timestamp_str]):
            # Missing required information, handle this case
            messages.error(request, 'Missing required information.')
            return render(request, 'auth/reset-password.html', context)

        if new_password != confirm_password:
            # Passwords do not match, handle this case
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/reset-password.html', context)

        # Convert the stored timestamp string into a datetime object
        stored_timestamp = timezone.datetime.strptime(stored_timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

        # Check if the OTP matches and it's within the 1 hour time limit
        if otp == stored_otp and timezone.now() - stored_timestamp <= timedelta(hours=1):
            # The OTP is valid and not expired, update the user's password

            # Hash the new password
            hashed_password = make_password(new_password)

            # Check the role and update the password accordingly
            if role.lower() in ['facultyandstaff', 'dean', 'bu']:
                # Update the password for a FacultyStaff user
                user = FacultyStaff.objects.get(email=email)
                user.password = hashed_password
                user.save()
            elif role.lower() in ['kaistaff', 'hkai']:
                # Update the password for a Kaibuemployee user
                user = Kaibuemployee.objects.get(email=email)
                user.password = hashed_password
                user.save()
            else:
                # Invalid role, handle this case
                messages.error(request, 'Invalid role.')
                return render(request, 'auth/reset-password.html', context)

            # Clear the OTP and timestamp from the session
            del request.session['otp']
            del request.session['otp_timestamp']

            messages.success(request, 'Password reset successful.')
            return redirect('app:login')  # Redirect to logout view

        else:
            # The OTP is invalid or expired, handle this case
            messages.error(request, 'Invalid or expired OTP.')
            return render(request, 'auth/reset-password.html', context)

    else:
        # If it's not a POST request, render the password reset form
        return render(request, 'auth/reset-password.html', context)







