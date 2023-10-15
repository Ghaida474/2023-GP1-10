from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .forms import Loginform  # Import your login form
from .models import Admin, FacultyStaff, Kaibuemployee

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

            user = authenticate(request, email=email, password=password)
  
            if user is not None:
                login(request, user)
                # Redirect to the appropriate page based on the user's type
                if user.position == 'staff' or user.position == 'faculty' :
                    return redirect('faculty_staff_account:faculty_staff_home')
                elif user.kaiposition == 'staff':
                    return redirect('kaistaff_account:kaistaff-home')
                elif user.kaiposition == 'head':
                    return redirect('kai_account:kai-home')
                elif  user.position == 'dean':
                    return redirect('dean_account:dean-account-home')
                elif  user.position == 'headofbu':
                    return redirect('business_unit_account:business-unit-home')   
            # Authentication failed
            messages.error(request, 'Invalid email, password.')

        else:
            messages.error(request, 'Form is invalid. Please check your input.')

    else:
        form = Loginform()

    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.error(request, 'You have been logged out successfully.')
    return redirect('app:login')  
