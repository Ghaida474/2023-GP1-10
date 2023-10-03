from django.shortcuts import render
from django.views import View

# main page

def index (request): 
    return render(request, 'index.html')

def services (request): 
    return render(request, 'services.html')

def contact (request): 
    return render(request, 'contact.html')

###################### 
def Home (request): 
    return render(request, 'hr-dashboard/index.html')

def client_list (request): 
    return render(request, 'client-dashboard/client-list.html')    

def client_new (request): 
    return render(request, 'client-dashboard/client-new.html')

def client_profile (request): 
    return render(request, 'client-dashboard/client-profile.html')

def client_view (request): 
    return render(request, 'client-dashboard/client-view.html')    

def index5 (request): 
    return render(request, 'client-dashboard/index5.html')

def index4 (request): 
    return render(request, 'project-dashboard/index4.html')

def project_list (request): 
    return render(request, 'project-dashboard/project-list.html')

def project_new (request): 
    return render(request, 'project-dashboard/project-new.html')

def project_overclndr (request): 
    return render(request, 'project-dashboard/project-overclndr.html')

def project_view (request): 
    return render(request, 'project-dashboard/project-view.html')

def edit_profile (request): 
    return render(request, 'edit-profile.html')
       
def empty_page (request): 
    return render(request, 'empty-page.html')

def forgot_password_1 (request): 
    return render(request, 'forgot-password-1.html')

def login_1 (request): 
    return render(request, 'login-1.html')

def profile_1 (request): 
    return render(request, 'profile-1.html')

def reset_password_1 (request): 
    return render(request, 'reset-password-1.html')

def settings (request): 
    return render(request, 'settings.html')


def chat (request): 
    return render(request, 'chat.html')
