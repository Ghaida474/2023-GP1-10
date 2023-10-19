from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from app.forms import updateFASform
from django.contrib.auth.decorators import login_required


@login_required
def faculty_staff_home (request):
    user = request.user
    context = {'user': user }
    return render(request, 'faculty_staff/empty-page.html', context)
    
    
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'faculty_staff/profile.html' ,{'user': user}) 

@login_required
def emptypage_view (request):
     return render(request, 'faculty_staff/empty-page.html') 

'''def editprofile_view(request):
    user = request.user

        if request.method == 'POST':
            form = updateFASform(request.POST, request.FILES, instance=user)

            if form.is_valid():
                    # Process other form fields
                    user.firstname = form.cleaned_data.get('firstname')
                    user.lastname = form.cleaned_data.get('lastname')
                    user.phonenumber = form.cleaned_data.get('phonenumber')
                    user.email = form.cleaned_data.get('email')
                    user.specialization = form.cleaned_data.get('specialization')
                    user.workstatus = form.cleaned_data.get('workstatus')
                    user.iban = form.cleaned_data.get('iban')
                    user.officeno = form.cleaned_data.get('officeno')
                    user.previouswork = form.cleaned_data.get('previouswork')

                    user.save()  # Save the user instance

            return redirect('faculty_staff_account:profile')

        else:
            form = updateFASform(instance=user)

        return render(request, 'edit-profile.html', {'form': form, 'user_id': user_id})

    else:
        # Handle the case when there's no user ID
        return HttpResponse("User not found or not logged in.")'''

@login_required
def editprofile_view(request):
        user = request.user
        if request.method == 'POST':
            form = updateFASform(request.POST, request.FILES, instance=user)

            if form.is_valid():
                # Process the file upload (CV field)
                cv_file = form.cleaned_data.get('cv')
                if cv_file:
                    user.cv = cv_file.read()
                # Process other form fields
                user.firstname = form.cleaned_data.get('firstname')
                user.lastname = form.cleaned_data.get('lastname')
                user.phonenumber = form.cleaned_data.get('phone_number')
                user.email = form.cleaned_data.get('email')
                user.specialization = form.cleaned_data.get('specialization')
                user.workstatus = form.cleaned_data.get('workstatus')
                user.iban = form.cleaned_data.get('iban')
                user.officeno = form.cleaned_data.get('officeno')
                user.previouswork = form.cleaned_data.get('previouswork')

                user.save()  # Save the user instance
                return redirect('faculty_staff_account:profile')
        else:
            form = updateFASform(instance=user)
            return render(request, 'faculty_staff/edit-profile.html', {'form': form, 'user': user})

