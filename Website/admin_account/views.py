from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
# from app.models import Admin
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from app.forms import adminform ,FASform,Loginform


'''# @login_required
def admin_home (request):
    user_id = request.session.get('user_id')
    if user_id:
        # Retrieve the user object using the user ID
        user = Admin.objects.get(pk=user_id)
        form2 = FASform(request.POST or None)
        if request.method == 'POST' and form2.is_valid():

            emaill = form2.cleaned_data.get('email')
            passw = form2.cleaned_data.get('password')
            fname = form2.cleaned_data.get('firstname')
            lname = form2.cleaned_data.get('lastname')
            phoneNumber = form2.cleaned_data.get('phonenumber')
            Gender = form2.cleaned_data.get('gender')
            Nationality = form2.cleaned_data.get('nationality')
            adminemail = form2.cleaned_data.get('adminemail')
            employeeid = form2.cleaned_data.get('employeeid')
            position = form2.cleaned_data.get('position')
            major = form2.cleaned_data.get('major')
            collage = form2.cleaned_data.get('collage')

            newFacultyAndStaff = FacultyAndStaff(
                email=emaill, password=make_password(passw), firstname=fname, lastname=lname,
                phonenumber=phoneNumber, gender=Gender, nationality=Nationality, adminemail=adminemail,
                employeeid=employeeid, position=position, major=major , collage=collage
            )
            newFacultyAndStaff.save()
            messages.success(request ,'user created')
        else:
            form1 = adminform()
        # Now you can access user information in your template
        return render(request, 'add-SANDF.html', {'user': user , 'form2': form2})
    else:
        form = Loginform()
        return render(request, 'app:login' ,{'form': form}) 


def addAdmin(request):

    form1 = adminform(request.POST or None)
    if request.method == 'POST' and form1.is_valid():
    
            email = form1.cleaned_data.get('email')
            password = form1.cleaned_data.get('password')

            newadmin = Admin(email=email , password =make_password(password))
            print(email,password)
    
            newadmin.save()
            messages.success(request ,'user created')
    else:
        form1 = adminform()

    return render(request, 'add-admin.html', {'form1': form1})'''
          
'''def addSANDF (request):
    form2 = FASform(request.POST or None)
    if request.method == 'POST' and form2.is_valid():

        emaill = form2.cleaned_data.get('email')
        passw = form2.cleaned_data.get('password')
        fname = form2.cleaned_data.get('firstname')
        lname = form2.cleaned_data.get('lastname')
        phoneNumber = form2.cleaned_data.get('phonenumber')
        Gender = form2.cleaned_data.get('gender')
        Nationality = form2.cleaned_data.get('nationality')
        adminemail = form2.cleaned_data.get('adminemail')
        employeeid = form2.cleaned_data.get('employeeid')
        position = form2.cleaned_data.get('position')
        major = form2.cleaned_data.get('major')
        collage = form2.cleaned_data.get('collage')

        newFacultyAndStaff = FacultyAndStaff(
            email=emaill, password=make_password(passw), firstname=fname, lastname=lname,
            phonenumber=phoneNumber, gender=Gender, nationality=Nationality, adminemail=adminemail,
            employeeid=employeeid, position=position, major=major , collage=collage
        )
        newFacultyAndStaff.save()
        messages.success(request ,'user created')
    else:
         form2 = FASform()
    return render(request, 'add-SANDF.html', {'form2': form2})'''