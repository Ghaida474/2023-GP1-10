from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff



@login_required
def business_unit_home (request):
    user = request.user
    context = {'user': user }

    return render(request, 'bu/Home.html', context)
    
    
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'bu/profile.html' ,{'user': user}) 

@login_required
def facultylist_view (request):
    user = request.user
    faculty = FacultyStaff.objects.all(collage =user.collage)
    
    return render(request, 'bu/faculty-list.html', {'faculty' : faculty})