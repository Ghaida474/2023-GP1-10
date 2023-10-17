from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .forms import Loginform  # Import your login form
from .models import Admin, FacultyStaff, Kaibuemployee
from django.conf import settings

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

