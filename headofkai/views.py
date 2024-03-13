from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from app.forms import updateKai,ChangePasswordForm
from app.models import FacultyStaff
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
    users = filteredUsers(request)
    return render(request, 'kai/chat.html' , {'username':username , 'secret': secret ,'users':users})

@login_required
def myChat(request):
    url = "https://api.chatengine.io/chats/"

    payload = {}
    headers = {
        'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
        'User-Name': request.user.username,
        'User-Secret': str(request.user.id),
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status() 

        users = response.json()
        my_users = []

        for user_data in users:
            people_data = user_data.get('people', [])
            for person_data in people_data:
                person = person_data.get('person', {})
                username = person.get('username', '')
                my_users.append({'username': username})

        return my_users

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []


@login_required
def filteredUsers(request):
    mychat = myChat(request)
  
    print("my_fi")
    # print(mychat)
    url = "https://api.chatengine.io/users/"
    payload = {}
    headers = {'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'}

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        users = response.json()
        matching_users = []
        # print('users' , users)
        for checkuser in users:
            if checkuser['username'] not in [entry['username'] for entry in mychat]:

                try:
                    newuser = FacultyStaff.objects.get(username=checkuser['username'])
                except FacultyStaff.DoesNotExist:
                    newuser = None 

                if newuser: 
                    if  newuser.position == 'عميد الكلية' or newuser.is_buhead:
                        matching_users.append({'username': checkuser.get('username'), 'secret': checkuser.get('secret'),'first_name':checkuser.get('first_name'),'last_name':checkuser.get('last_name')})
                else:
                    if checkuser['username'] != request.user.id:
                        matching_users.append({'username': checkuser.get('username'), 'secret': checkuser.get('secret'),'first_name':checkuser.get('first_name'),'last_name':checkuser.get('last_name')})

        # print("Matching users:", matching_users)
        return matching_users

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []
    
@login_required
def createDirect(request,direct_username):
    url = "https://api.chatengine.io/chats/"
    payload = {
        "title": direct_username,
        "is_direct_chat": False,
        "usernames":direct_username    
    }
    headers = {
        'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
        'User-Name':  request.user.username,
        'User-Secret': str(request.user.id),
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    responseINjson = response.json()
    users = filteredUsers(request)
    context = {'username': request.user.username , 'secret' :request.user.id , 'users':users }
    return render(request, 'kai/chat.html' , context)


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

