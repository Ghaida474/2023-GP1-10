from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff


@login_required
def dean_account_home (request):
    user = request.user
    context = {'user': user }
    return render(request, 'dean/empty-page.html', context)
      
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'dean/profile.html' ,{'user': user}) 

@login_required
def emptypage_view(request):
    user = request.user
    return render(request, 'dean/empty-page.html' ,{'user': user}) 

@login_required
def facultylist_view (request):
    user = request.user
    faculty = FacultyStaff.objects.filter(collageid =user.collageid)
    
    return render(request, 'dean/faculty-list.html', {'faculty' : faculty})