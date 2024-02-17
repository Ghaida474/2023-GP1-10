from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.forms import updateKai,ChangePasswordForm
from django.contrib.auth import update_session_auth_hash


@login_required
def callsDashboard(request):
    return render(request, 'kai/calls-dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    return render(request, 'kai/videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

@login_required
def joinroom(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/head-kai-account/kai-home/videocall?roomID=" + roomID)
    return render(request, 'kai/joinroom.html')

@login_required
def chat(request):
    username = request.user.username
    secret = request.user.id
    return render(request, 'kai/chat.html' , {'username':username , 'secret': secret })

@login_required
def kai_home (request):
    user = request.user
    return render(request, 'kai/Home.html', {'user': user })
      
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'kai/profile.html' ,{'user': user}) 


@login_required
def editprofile_view(request):
    user = request.user
    form = updateKai(instance=user)
    success = False
    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'form1': 
            form = updateKai(request.POST, request.FILES, instance=user)   
            if form.is_valid():    
                form.save()
                success = True
            
    return render(request, 'kai/edit-profile.html', {'form': form , 'user' : user , 'success':success})


@login_required
def changepassword_view(request):
    user = request.user
    form = ChangePasswordForm(user)
    success = False
    if request.method == 'POST':
        print('here1')
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            success = True

    return render(request, 'kai/change-password.html', {'user': user, 'form': form , 'success':success})

@login_required
def projectpage(request):
    return render(request, 'kai/project/project-list.html')

