from django.shortcuts import render
from django.views import View

# main page

def index (request): 
    return render(request, 'index.html')
 
def Home (request): 
    return render(request, 'home.html')

def facultylist (request): 
    return render(request, 'faculty-list.html')    

def facultyview (request): 
    return render(request, 'faculty-view.html')    

def project_list (request): 
    return render(request, 'project/project-list.html')

def project_new (request): 
    return render(request, 'project/project-new.html')

def project_overclndr (request): 
    return render(request, 'project/project-overclndr.html')

def project_view (request): 
    return render(request, 'project/project-view.html')

def edit_profile (request): 
    return render(request, 'edit-profile.html')
       
def empty_page (request): 
    return render(request, 'empty-page.html')

def forgot_password (request): 
    return render(request, 'forgot-password.html')

def login (request): 
    return render(request, 'login.html')

def profile (request): 
    return render(request, 'profile.html')

def reset_password (request): 
    return render(request, 'reset-password.html')

def settings (request): 
    return render(request, 'settings.html')

def chat (request): 
    return render(request, 'chat.html')
