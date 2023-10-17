from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff



@login_required
def kai_home (request):
    user = request.user
    return render(request, 'kai/empty-page.html', {'user': user })
      
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'kai/profile.html' ,{'user': user}) 

