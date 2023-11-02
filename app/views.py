from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .forms import Loginform 
from .models import Admin, FacultyStaff, Kaibuemployee
from django.conf import settings
from .forms import ForgetPasswordForm
from django.core.mail import send_mail
import random
import string
import smtplib
import ssl
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import emailcheckform
import certifi
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import authenticate, login
def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

def index(request):
    return render(request, 'auth/index.html')



def login_view(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            next_url = request.POST.get('next')

            # Check if the email exists in the correct model based on the role
            if role in ['facultyandstaff', 'dean', 'BU']:
                if FacultyStaff.objects.filter(email=email).exists():
                    user = authenticate(request, email=email, password=password)
                elif Kaibuemployee.objects.filter(email=email).exists():
                    clear_messages(request)
                    messages.error(request, 'فئة المستخدم غير صحيحة')
                    return render(request, 'auth/login.html', {'form': form})
 
            elif role in ['kaistaff', 'Hkai']:
                if Kaibuemployee.objects.filter(email=email).exists():
                    user = authenticate(request, email=email, password=password)
                elif FacultyStaff.objects.filter(email=email).exists():
                    clear_messages(request)
                    messages.error(request, 'فئة المستخدم غير صحيحة')
                    return render(request, 'auth/login.html', {'form': form})

            else:
                clear_messages(request)
                messages.error(request, 'البريد الإلكتروني غير صحيح.')
                return render(request, 'auth/login.html', {'form': form})



            if user is not None:
                if role == 'facultyandstaff' and (user.position == 'عضو هيئة التدريس' or user.position == 'موظف في الكلية'):
                    login(request, user)
                    return redirect('faculty_staff_account:faculty_staff_home')
                elif  role == 'dean' and user.position == 'عميد الكلية':
                    login(request, user)
                    return redirect('dean_account:dean-account-home')
                elif  role == 'BU' and user.is_buhead == True:
                    login(request, user)
                    return redirect('business_unit_account:business_unit_home')
                elif role == 'kaistaff' and user.position == 'موظف في المعهد':
                    login(request, user)
                    return redirect('kai_staff:kaistaff-home')
                elif role == 'Hkai' and user.position == 'رئيس المعهد':
                    login(request, user)
                    return redirect('head-kai-account:kai-home')
                else:
                    clear_messages(request)
                    messages.error(request, 'فئة المستخدم غير صحيحة')
            else:              
                if Kaibuemployee.objects.filter(email=email).exists() or FacultyStaff.objects.filter(email=email).exists():
                    clear_messages(request)
                    messages.error(request, 'كلمة السر غير صحيحة.')
                else:
                    clear_messages(request)
                    messages.error(request, ' البريد الإلكتروني غير صحيح.')
            return render(request, 'auth/login.html', {'form': form})
        else:
            clear_messages(request)
            messages.error(request,'خطأ ما حصل وقت الارسال حاول تسجيل الدخول مره آخرى')
            form = Loginform()
            return render(request, 'auth/login.html', {'form': form })
    else:
        form = Loginform()
        return render(request, 'auth/login.html', {'form': form })
# def forgot_password(request):
#     #form = ForgetPasswordForm()
#     form = Loginform()
#     return render(request, 'auth/forgot-password.html', {'form':form} )

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

        if role == 'facultyandstaff' and user.position in ['عضو هيئة التدريس', 'موظف في الكلية']:
            print("Matched FacultyStaff with position 'facultyandstaff'")
            return True


    if role == 'dean' and user.position == 'عميد الكلية':
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

        if role == 'kaistaff' and user.position == 'موظف في المعهد':
            print("Matched Kaibuemployee with position 'kaistaff'")
            return True

        if role == 'hkai' and user.position == 'رئيس المعهد':
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
                if Kaibuemployee.objects.filter(email=email).exists() or FacultyStaff.objects.filter(email=email).exists():
                    clear_messages(request)
                    messages.error(request, 'فئة المستخدم غير صحيحة')
                else:
                    clear_messages(request)
                    messages.error(request, ' البريد الإلكتروني غير صحيح.')
        
    form = emailcheckform()
    return render(request, 'auth/forgot-password.html', {'form': form})


def send_email_to_reset_password(request, email, role):
    context = {
        'email': email,
        'role': role,
    }
    print("send email function entered successfully")
    print("receiver email", email)

    # Generate a 6-digit OTP
    otp = ''.join(random.choice(string.digits) for _ in range(6))
    print(otp)

    # Construct the email message
    subject = 'Password Reset OTP'
    message = 'Subject: {}\n\nYour OTP for password reset is: {}\n\nYour OTP is valid for 10 minutes. If the OTP expires before you reset your password, please navigate to the Sign In page to generate a new one.'.format(subject, otp)
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
    # Retrieve password and otp from post data
    entered_otp = request.POST.get('otp')
    new_password = request.POST.get('new_password')

    # Retrieve OTP and its timestamp from session
    session_otp = request.session.get('otp')
    otp_timestamp_str = request.session.get('otp_timestamp')

    # Remove ":" from the timezone offset
    otp_timestamp_str = otp_timestamp_str.replace("+00:00", "+0000")

    # Now parse the timestamp
    otp_timestamp = datetime.strptime(otp_timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

    if timezone.now() - otp_timestamp > timedelta(minutes=10):
        # OTP expired, delete it from session
        del request.session['otp']
        del request.session['otp_timestamp']

        # Send a new OTP
        send_email_to_reset_password(request, email, role)

        # Show a message for expired OTP
        clear_messages(request)
        messages.error(request, 'انتهت صلاحية كلمة المرور لمرة واحدة(OTP)، وتم إرسال كلمة مرور لمرة واحدة جديدة إلى بريدك الإلكتروني.')
        return reset_password(request, email, role)
    else:
        # OTP not expired
        if entered_otp != session_otp:
            # Entered OTP does not match the one in session
            del request.session['otp']
            del request.session['otp_timestamp']

            # Send a new OTP
            send_email_to_reset_password(request, email, role)

            # Show a message for incorrect OTP
            clear_messages(request)
            messages.error(request, 'كلمة مرور لمرة واحدة غير صحيحة(OTP)، تم إرسال كلمة مرور لمرة واحدة جديدة إلى بريدك الإلكتروني.')
            return reset_password(request, email, role)
        else:
            # OTP matches, delete it from session
            del request.session['otp']
            del request.session['otp_timestamp']

            # Handle different roles
            if role.lower() in ['facultyandstaff', 'dean', 'bu']:
                user = FacultyStaff.objects.get(email=email)
            elif role.lower() in ['kaistaff', 'hkai']:
                user = Kaibuemployee.objects.get(email=email)

            # Set the new password
            user.set_password(new_password)
            user.save()

            # Show a message for successful password reset
            clear_messages(request)
            messages.error(request, 'تم إعادة تعيين كلمة المرور بنجاح.')
            return redirect('app:login')
            # Show a message for incorrect OTP


def logout_view(request):
    logout(request)
    clear_messages(request)
    messages.error(request, 'لقد تم تسجيل خروجك بنجاح.')
    return redirect('app:login')