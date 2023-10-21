from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff,Collage
from app.forms import updateFASform,previousworkform,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages


@login_required
def kaistaff_home (request):
    user = request.user
    return render(request, 'kai-staff/empty-page.html', {'user': user })
      

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'kai-staff/profile.html' ,{'user': user}) 


@login_required
def editprofile_view(request):
    user = request.user
    form = updateFASform(instance=user)
 
    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'form1': 
            form = updateFASform(request.POST, instance=user)   
            if form.is_valid():  
                    
                form.save()
                return redirect('kaistaff_account:profile')
            
    return render(request, 'kai-staff/edit-profile.html', {'form': form , 'user' : user})



def changepassword_view(request):
    user = request.user
    form = ChangePasswordForm(user)
    
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            # messages(request, 'Password changed successfully.') 
            return redirect('kaistaff_account:profile')

    return render(request, 'kai-staff/change-password.html', {'user': user, 'form': form})
