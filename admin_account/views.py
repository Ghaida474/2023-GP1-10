from django.utils import timezone
from datetime import date, datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from app.models import Admin, FacultyStaff ,Collage,Kaibuemployee,Trainingprogram,Project, Task ,TaskToUser
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import string
import secrets
import requests

from django.conf import settings
from django.core.mail import send_mail
import smtplib
import ssl
import certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db import connection


@login_required
def admin_home (request):
    collage = Collage.objects.count()
    facultyStaff = FacultyStaff.objects.count()
    kaibuemployee = Kaibuemployee.objects.count()
    return render(request, 'admin/Home.html' , {'collage':collage , 'FacultyStaff':facultyStaff, 'Kaibuemployee':kaibuemployee })

@login_required
def addFaculty (request):
    nationalities = getnationalities()
    collage = Collage.objects.all()
    if request.method == 'POST':
      firstName = request.POST.get('firstName')
      lastName = request.POST.get('lastName')
      firstNameENG = request.POST.get('firstNameENG')
      lastNameENG = request.POST.get('lastNameENG')
      email = request.POST.get('email')
      phonenumber = request.POST.get('phonenumber')
      gender = request.POST.get('gender')
      nationality = request.POST.get('nationality')
      collageid = request.POST.get('collage')
      deparment = request.POST.get('deparment')
      position = request.POST.get('position')
      rank = request.POST.get('rank')
      empNum = request.POST.get('empNum')
      isbu = request.POST.get('isbu')
      assistant = request.POST.get('assistant')

      if isbu:
          isbu=True
      else:
          isbu=False

      if assistant:
          assistant=True
      else:
          assistant=False

      random_password = generate_random_password()
      print(random_password)
      password = random_password
      random_password = make_password(random_password)

      username = email.split('@')

      getcollage = Collage.objects.get(collageid=collageid)
      
      new_faculty = FacultyStaff(
            password = random_password,
            is_superuser = False,
            first_name = firstName,
            last_name = lastName,
            email = email,
            is_active = True,
            phonenumber = phonenumber,
            gender =  gender,
            nationality = nationality,
            adminemail = request.user.email,
            is_staff = True,
            employeeid = empNum,
            position = position, 
            major = deparment,
            collageid = getcollage,
            is_buhead = isbu, 
            bu_assistant = assistant,
            username = username[0],
            department_field = deparment,
            rank = rank,
            first_nameeng = firstNameENG,
            last_nameeng = lastNameENG,
            workstatus = 'على رأس العمل',
            date_joined = timezone.now().date() ,
      )
      new_faculty.save()
      print('new_faculty',new_faculty)

      send_email_to_new_user(request , email , password , new_faculty.is_buhead )

      firstname = new_faculty.first_name + ' '+ new_faculty.last_name
      lastname = ' | ' + new_faculty.position
      if new_faculty.is_buhead:
        name = "رئيس وحدة الاعمال في "+ getcollage.name
        lastname = ' | ' + name
          
      url = "https://api.chatengine.io/users/"
      payload = {
          "username":username[0],
          "first_name":firstname,
          "last_name":lastname,
          "secret": new_faculty.id,
          "email" : email,
          "custom_json": {"high_score": 2000},
      }
      headers = {
        'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'
        }
      response = requests.request("POST", url, headers=headers, data=payload)
      print(response.text)

      return redirect('admin_account:facultyList')
    return render(request, 'admin/addFaculty.html' ,{'collage':collage ,'nationalities':nationalities})

@login_required
def addKai (request):
    nationalities = getnationalities()
    if request.method == 'POST':
      firstName = request.POST.get('firstName')
      lastName = request.POST.get('lastName')
      email = request.POST.get('email')
      phonenumber = request.POST.get('phonenumber')
      gender = request.POST.get('gender')
      nationality = request.POST.get('nationality')
      position = request.POST.get('position')
      empNum = request.POST.get('empNum')

      random_password = generate_random_password()
      print(random_password)
      password = random_password 
      random_password = make_password(random_password)

      username = email.split('@')

      new_kai = Kaibuemployee(
            password = random_password,
            is_superuser = False,
            first_name = firstName,
            last_name = lastName,
            email = email,
            is_active = True,
            phonenumber = phonenumber,
            gender =  gender,
            nationality = nationality,
            adminemail = request.user.email,
            is_staff = True,
            kaiemployeeid = empNum,
            position = position, 
            username = username[0],
            date_joined = timezone.now().date() ,
      )
      new_kai.save()
      print('new_kai',new_kai)

      send_email_to_new_user(request , email , password)

      firstname = new_kai.first_name + ' '+ new_kai.last_name
      lastname = ' | ' + new_kai.position

      url = "https://api.chatengine.io/users/"
      payload = {
          "username":username[0],
          "first_name":firstname,
          "last_name":lastname,
          "secret": new_kai.id,
          "email" : email,
          "custom_json": {"high_score": 2000},
      }
      headers = {
        'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'
        }
      response = requests.request("POST", url, headers=headers, data=payload)
      print(response.text)

      return redirect('admin_account:kaiList')
    return render(request, 'admin/addKai.html' , {'nationalities':nationalities})

@login_required
def addCollage (request):
    collage = Collage.objects.all()
    if request.method == 'POST':
            name = request.POST.get('name')
            nofaculty = request.POST.get('nofaculty2')
            nostaff = request.POST.get('nofaculty')
            nofemalestudents = request.POST.get('nofemalestudents')
            nomalestudents = request.POST.get('nomalestudents')
            nofloor = request.POST.get('floor')
            nodisk = request.POST.get('disknum')
            nobuilding = request.POST.get('buildingnum')
            buemail = request.POST.get('buemail')
            buphonenumber = request.POST.get('buphonenumber')
            domain = request.POST.getlist('domains[]')
            departments =  request.POST.getlist('departments[]')
            domain.append("اخرى")

            if nofemalestudents:
                nofemalestudents = int(nofemalestudents) 
            else:
                nofemalestudents = None
            
            if nomalestudents:
                nomalestudents = int(nomalestudents) 
            else:
                nomalestudents = None
            
            if nofaculty:
                nofaculty = nofaculty
            else:
                nofaculty = None
            
            if nostaff:
                nostaff = nostaff
            else:
                nostaff = None

            nostudents = 0
            if nomalestudents and nofemalestudents:
                nostudents = int(nofemalestudents) + int(nomalestudents)
            elif nomalestudents:
                nostudents = int(nomalestudents)
            elif nofemalestudents:
                nostudents = int(nofemalestudents)
            else:
                nostudents = None
                
            if nodisk:
                nodisk = nodisk
            else:
                nodisk = None
            
            if nobuilding:
                nobuilding = nobuilding
            else:
                nobuilding = None

            new_collage = Collage(
                name = name,
                adminemail = request.user,
                nofaculty = nofaculty,
                nostaff = nostaff,
                nostudents = nostudents,
                nofemalestudents = nofemalestudents,
                nomalestudents = nomalestudents,
                buemail = buemail,
                buphonenumber = buphonenumber,
                departments = departments,
                domain = domain,
                nobuilding = nobuilding,
                nodisk = nodisk,
                nofloor = nofloor ,
                new_user = True,
                last_update = timezone.now(),
            )
            new_collage.save()
            print('new_collage',new_collage)
            return redirect('admin_account:collageList')
           
    return render(request, 'admin/addCollage.html' ,{'collage':collage} )

@login_required
def facultyList (request):
    facultyList = FacultyStaff.objects.all()
    collages = Collage.objects.all()
    return render(request, 'admin/facultyList.html' ,{'facultyList':facultyList , 'collages':collages} )

@login_required
def kaiList (request):
    # kai = Kaibuemployee.objects.get(id = 47)
    # kai.delete()
    kaiList = Kaibuemployee.objects.all()
    return render(request, 'admin/kaiList.html' ,{'kaiList':kaiList} )

@login_required
def collageList (request):
    collageList = Collage.objects.all()
    # collage = Collage.objects.get(collageid = 19)
    # collage.delete()
    return render(request, 'admin/collageList.html' ,{'collageList':collageList} )

@login_required
def editfaculty (request , id ):
    collage = Collage.objects.all()
    nationalities = getnationalities()
    facultyexists = (
    Trainingprogram.objects.filter(instructorid__contains=[id]).exists() or
    Project.objects.filter(Teamid__contains=[id]).exists()
    )
    getcollage = FacultyStaff.objects.get(id=id)
    buexists = FacultyStaff.objects.filter(id=id, is_buhead=True, collageid=getcollage.collageid).exists()
    print('buexists',buexists)
    try:
        editfaculty = FacultyStaff.objects.get(id=id)
        if request.method == 'POST':
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            firstNameENG = request.POST.get('firstNameENG')
            lastNameENG = request.POST.get('lastNameENG')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phonenumber')
            gender = request.POST.get('gender')
            nationality = request.POST.get('nationality')
            collageid = request.POST.get('collage')
            deparment = request.POST.get('deparment')
            position = request.POST.get('position')
            rank = request.POST.get('rank')
            empNum = request.POST.get('empNum')
            isbu = request.POST.get('isbu')
            assistant = request.POST.get('assistant')
            
            if editfaculty.is_buhead is False and isbu:
                send_email_to_new_BU(request , editfaculty.email)

            if isbu:
                isbu=True
            else:
                isbu=False

            if assistant:
                assistant=True
            else:
                assistant=False

            username = email.split('@')
            getcollage = Collage.objects.get(collageid=collageid)
            oldussername = editfaculty.username
            
            editfaculty.first_name = firstName
            editfaculty.last_name = lastName
            editfaculty.email = email
            editfaculty.phonenumber = phonenumber
            editfaculty.gender =  gender
            editfaculty.nationality = nationality
            editfaculty.adminemail = request.user.email
            editfaculty.employeeid = empNum
            editfaculty.position = position 
            editfaculty.major = deparment
            collageid = getcollage
            editfaculty.is_buhead = isbu
            editfaculty.bu_assistant = assistant
            editfaculty.username = username[0]
            editfaculty.department_field = deparment
            editfaculty.rank = rank
            editfaculty.first_nameeng = firstNameENG
            editfaculty.last_nameeng = lastNameENG
            editfaculty.save()
            facultyUpdateapi(request , editfaculty , oldussername)
            print('editfaculty',editfaculty)
            return redirect('admin_account:facultyList')
    except Exception as e:
        print('Error occurred:', e)
    return render(request, 'admin/editfaculty.html' ,{ 'buexists':buexists, 'facultyexists':facultyexists, 'editfaculty':editfaculty , 'nationalities':nationalities , 'collage':collage} )

@login_required
def editkai (request , id ):
    nationalities = getnationalities()
    kai = Kaibuemployee.objects.get(id=id)
    kaiexists = (Task.objects.filter(kai_initiation = kai).exists() or
                 Task.objects.filter(kai_ids__contains=[kai.id]).exists() or
                 TaskToUser.objects.filter(kai_user= kai).exists() 
                 )
    try:
        editkai = Kaibuemployee.objects.get(id=id)
        if request.method == 'POST':
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phonenumber')
            gender = request.POST.get('gender')
            nationality = request.POST.get('nationality')
            position = request.POST.get('position')
            empNum = request.POST.get('empNum')      
            username = email.split('@')
            oldussername = editkai.username

            editkai.first_name = firstName
            editkai.last_name = lastName
            editkai.email = email
            editkai.phonenumber = phonenumber
            editkai.gender =  gender
            editkai.nationality = nationality
            editkai.adminemail = request.user.email
            editkai.kaiemployeeid = empNum,
            editkai.position = position
            editkai.username = username[0]
            editkai.save()
            kaiUpdateapi(request , editkai , oldussername)
            print('editkai',editkai)
            return redirect('admin_account:kaiList')
    except Exception as e:
        print('Error occurred:', e)
    return render(request, 'admin/editkai.html' ,{'kaiexists':kaiexists ,'editkai':editkai , 'nationalities':nationalities} )

def facultyUpdateapi(request , user , oldussername):
    # 1
    print('oldussername' , oldussername)
    print('user.username' , user.username)
    url = "https://api.chatengine.io/users/"
    payload={}
    headers = {
    'PRIVATE-KEY':'499cc31a-d338-455c-8e1c-7ea6e54afc38'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print('first *******************************************')
    # print(response.text)
    if response.status_code == 200:
        user_data = response.json()
        user_id = None
        
        for user_info in user_data:
            print('user_info.get("username")' , user_info.get("username"))
            if user_info.get("username") == oldussername:
                user_id = user_info.get("id")
                break
        
        if user_id is not None:
            print('user_id' , user_id)
            username = user.email.split('@')
            getcollage = Collage.objects.get(collageid= user.collageid.collageid)
            firstname = user.first_name + ' '+ user.last_name
            lastname = ' | ' + user.position
            if user.is_buhead:
                name = "رئيس وحدة الاعمال في "+ getcollage.name
                lastname = ' | ' + name
            # 2
            url = f"https://api.chatengine.io/users/{user_id}/"
            payload = {"username":username[0] ,
                       "email": user.email ,
                        "first_name":firstname ,
                        "last_name":lastname,
                        "custom_json": {"high_score": 3000},
                        "is_online": True}
            headers = {
            'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'
            }
            response = requests.request("PATCH", url, headers=headers, data=payload)
            print('secound *******************************************')
            print(response.text)
        else:
            return HttpResponse("User ID not found.")
    else:
        return HttpResponse("Failed to fetch user data from API.")

def kaiUpdateapi(request , user , oldussername):
    url = "https://api.chatengine.io/users/"
    payload={}
    headers = {
    'PRIVATE-KEY':'499cc31a-d338-455c-8e1c-7ea6e54afc38'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        user_data = response.json()
        user_id = None
        
        for user_info in user_data:
            if user_info.get("username") == oldussername:
                user_id = user_info.get("id")
                break
        
        if user_id is not None:
            username = user.email.split('@')
            firstname = user.first_name + ' '+ user.last_name
            lastname = ' | ' + user.position
            
            url = f"https://api.chatengine.io/users/{user_id}/"
            payload = {"username":username[0] ,
                       "email": user.email ,
                        "first_name":firstname ,
                        "last_name":lastname,
                        "custom_json": {"high_score": 3000},
                        "is_online": True}
            headers = {
            'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'
            }
            response = requests.request("PATCH", url, headers=headers, data=payload)
            print(response.text)
        else:
            return HttpResponse("User ID not found.")
    else:
        return HttpResponse("Failed to fetch user data from API.")
    
@login_required
def editcollage (request , id ):
    try:
        editcollage = Collage.objects.get(collageid=id)
        facultyexists = FacultyStaff.objects.filter(collageid=editcollage).exists()

        if request.method == 'POST':
            name = request.POST.get('name')
            nofaculty = request.POST.get('nofaculty2')
            nostaff = request.POST.get('nofaculty')
            nofemalestudents = request.POST.get('nofemalestudents')
            nomalestudents = request.POST.get('nomalestudents')
            nofloor = request.POST.get('floor')
            nodisk = request.POST.get('disknum')
            nobuilding = request.POST.get('buildingnum')
            departments =  request.POST.getlist('departments[]')
            buemail = request.POST.get('buemail')
            buphonenumber = request.POST.get('buphonenumber')
            domain = request.POST.getlist('domains[]')

            if nofemalestudents:
                editcollage.nofemalestudents = int(nofemalestudents) 
            else:
                editcollage.nofemalestudents = None
            
            if nomalestudents:
                editcollage.nomalestudents = int(nomalestudents) 
            else:
                editcollage.nomalestudents = None
            
            if nofaculty:
                editcollage.nofaculty = nofaculty
            else:
                editcollage.nofaculty = None
            
            if nostaff:
                editcollage.nostaff = nostaff
            else:
                editcollage.nostaff = None

            if nomalestudents and nofemalestudents:
                editcollage.nostudents = int(nofemalestudents) + int(nomalestudents)
            elif nomalestudents:
                editcollage.nostudents = int(nomalestudents)
            elif nofemalestudents:
                editcollage.nostudents = int(nofemalestudents)
            else:
                editcollage.nostudents = None
                
            if nodisk:
                editcollage.nodisk = nodisk
            else:
                editcollage.nodisk = None
            
            if nobuilding:
                editcollage.nobuilding = nobuilding
            else:
                editcollage.nobuilding = None

            editcollage.name = name
            editcollage.adminemail = request.user
            editcollage.buemail = buemail
            editcollage.buphonenumber = buphonenumber
            editcollage.departments = departments
            editcollage.domain = domain
            editcollage.nofloor = nofloor
            editcollage.last_update = timezone.now()
            editcollage.save()
            print('editcollage', editcollage)
            return redirect('admin_account:collageList')

    except Exception as e:
        print('Error occurred:', e)
    return render(request, 'admin/editcollage.html' ,{'editcollage':editcollage , 'facultyexists':facultyexists} )

@login_required
def deletecollage (request , id ):
    collage = Collage.objects.get(collageid=id)
    collage.delete()
    return redirect('admin_account:collageList')

@login_required
def deletefaculty (request , id ):
    try:
            getusername = FacultyStaff.objects.get(id = id)
            deletefromApi(request , getusername.username)
            with connection.cursor() as cursor:
                 cursor.execute('DELETE FROM public."Faculty_Staff" WHERE id = %s', [id])           
            return redirect('admin_account:facultyList')
    except Exception as e:
            return HttpResponse(f"Error deleting record: {e}")

@login_required
def deletekai (request , id ):
    try:
            getusername = Kaibuemployee.objects.get(id = id)
            deletefromApi(request , getusername.username)
            with connection.cursor() as cursor:
                 cursor.execute('DELETE FROM public."KAIBUEmployee" WHERE id = %s', [id])           
            return redirect('admin_account:kaiList')
    except Exception as e:
            return HttpResponse(f"Error deleting record: {e}")

def deletefromApi(request , username):
    url = "https://api.chatengine.io/users/"
    payload={}
    headers = {
    'PRIVATE-KEY':'499cc31a-d338-455c-8e1c-7ea6e54afc38'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        user_data = response.json()
        user_id = None
        
        for user_info in user_data:
            if user_info.get("username") == username:
                user_id = user_info.get("id")
                break
        
        if user_id is not None:
            url = f"https://api.chatengine.io/users/{user_id}/"
            payload={}
            headers = {
            'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'
            }
            response = requests.request("DELETE", url, headers=headers, data=payload)
            print(response.text)

@login_required
def checkdepartment(request , department):
    try:
        checkIFdepartment = FacultyStaff.objects.filter(department_field = department).exists()
        if checkIFdepartment:
            return JsonResponse({'success_message': True})
    except FacultyStaff.DoesNotExist:
        pass  
    return JsonResponse({'success_message': False})

@login_required
def checkdomain(request , domain):
    try:
        checkIFdepartment = Trainingprogram.objects.filter(program_domain = domain).exists()
        if checkIFdepartment:
            return JsonResponse({'success_message': True})
    except FacultyStaff.DoesNotExist:
        pass  
    return JsonResponse({'success_message': False})

@login_required
def checkBU(request, collage_id):
    try:
        checkifBU = FacultyStaff.objects.get(collageid=collage_id, is_buhead=True)
        if checkifBU:
            return JsonResponse({'success_message': True})
    except FacultyStaff.DoesNotExist:
        pass  
    return JsonResponse({'success_message': False})

@login_required
def checkAssistant(request, collage_id):
    try:
        checkifAssistant = FacultyStaff.objects.get(collageid=collage_id, bu_assistant=True)
        if checkifAssistant:
            return JsonResponse({'success_message': True})
    except FacultyStaff.DoesNotExist:
        pass  
    return JsonResponse({'success_message': False})

@login_required
def checkEmail(request, email):
    try:
        checkifEmail = FacultyStaff.objects.filter(email=email).exists() or \
                       Kaibuemployee.objects.filter(email=email).exists()

        if checkifEmail:
            print('Email exists in either FacultyStaff or Kaibuemployee table')
            return JsonResponse({'success_message': True})
        else:
            print('Email does not exist in either FacultyStaff or Kaibuemployee table')
            return JsonResponse({'success_message': False})

    except Exception as e:
        print('Error occurred:', e)
        return JsonResponse({'success_message': False})

@login_required
def checkposition(request):
    try:
        checkifposition = Kaibuemployee.objects.filter(position = 'رئيس قسم وحدات الأعمال بمعهد الملك عبدالله').exists()
        if checkifposition:
            return JsonResponse({'success_message': True})
    except Kaibuemployee.DoesNotExist:
        pass  
    return JsonResponse({'success_message': False})

def generate_random_password(length=12):
    # Define the character set for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate the random password
    password = ''.join(secrets.choice(characters) for i in range(length))
    
    return password

@login_required
def send_email_to_new_user(request, email, password , is_buhead = None):
    body2 = ''
    if is_buhead:
        faculty = FacultyStaff.objects.get(email= email)
        collage = Collage.objects.get(collageid = faculty.collageid.collageid)
        bupassword = generate_random_password()
        collage.password = bupassword
        collage.userid = faculty.id
        collage.password = make_password(collage.password)
        collage.save()

        body2 = '''\
            <html>
            <body>
            <p align="right" dir="rtl">السلام عليكم،</p>

            <p align="right" dir="rtl">لقد تم تسجيلك في نظام بوابة الاعمال، لتسهيل تشغيل الاعمال في وحدات الاعمال في كليات جامعه الملك سعود  بإمكانك التسجيل عبر النظام بايميلك التابع للجامعه و كلمة المرور التالية:</p>

            <p align="right" dir="rtl">حسابك الشخصي:</p>
            <p align="right" dir="rtl">الايميل: {email}</p>
            <p align="right" dir="rtl">كلمة المرور: {password}</p>

            <p align="right" dir="rtl">حسابك كرئيس وحدة الاعمال:</p>
            <p align="right" dir="rtl">الايميل: {email2}</p>
            <p align="right" dir="rtl">كلمة المرور: {password2}</p>

            <p align="right" dir="rtl">عبر : ......</p>

            <p align="right" dir="rtl">شكراً لك،<br>فريق الدعم الخاص ببوابة الاعمال</p>
            

            </body>
            </html>
            '''.format(email=email, password=password , email2=collage.buemail , password2=bupassword)

    subject = 'مرحباً بك في بوابة الاعمال'

    body = '''\
    <html>
    <body>
    <p align="right" dir="rtl">السلام عليكم،</p>

    <p align="right" dir="rtl">لقد تم تسجيلك في نظام بوابة الاعمال، لتسهيل تشغيل الاعمال في وحدات الاعمال في كليات جامعه الملك سعود  بإمكانك التسجيل عبر النظام بايميلك التابع للجامعه و كلمة المرور التالية:</p>

    <p align="right" dir="rtl">الايميل: {email}</p>
    <p align="right" dir="rtl">كلمة المرور: {password}</p>

    <p align="right" dir="rtl">عبر : ......</p>

    <p align="right" dir="rtl">شكراً لك،<br>فريق الدعم الخاص ببوابة الاعمال</p>
    

    </body>
    </html>
    '''.format(email=email, password=password)

 
    # Create MIMEText object with body and charset
    body_mime = MIMEText(body, 'html', 'utf-8')
    if is_buhead:
        body_mime = MIMEText(body2, 'html', 'utf-8')

    myemail = "442200922@student.ksu.edu.sa"
    # Construct email with headers and body
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg['From'] = settings.EMAIL_HOST_USER
    email_msg['To'] = myemail
    email_msg.attach(body_mime)

    # Create the SSL context
    context = ssl.create_default_context(cafile=certifi.where())

    # Create connection
    connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    connection.starttls(context=context)

    # Login
    connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Send email
    connection.sendmail(settings.EMAIL_HOST_USER, [myemail], email_msg.as_string())

    # Close connection
    connection.quit()

    print("correctly entered the function")

    return HttpResponse("Password reset email sent.")

@login_required
def send_email_to_new_BU(request, email):
   
        faculty = FacultyStaff.objects.get(email= email)
        collage = Collage.objects.get(collageid = faculty.collageid.collageid)
        bupassword = generate_random_password()
        collage.password = bupassword
        collage.new_user = True
        collage.userid = faculty.id
        collage.password = make_password(collage.password)
        collage.save()

        subject = 'مرحباً بك في بوابة الاعمال'

        body = '''\
        <html>
        <body>
        <p align="right" dir="rtl">السلام عليكم،</p>

        <p align="right" dir="rtl">لقد تم تعيينك رئيس وحدة الاعمال في نظام بوابة الاعمال، لتسهيل تشغيل الاعمال في وحدات الاعمال في كليات جامعه الملك سعود.</p>

        <p align="right" dir="rtl"> حسابك كرئيس وحدة الاعمال: </p>
        <p align="right" dir="rtl">الايميل: {email}</p>
        <p align="right" dir="rtl">كلمة المرور: {password}</p>

        <p align="right" dir="rtl">عبر : ......</p>

        <p align="right" dir="rtl">شكراً لك،<br>فريق الدعم الخاص ببوابة الاعمال</p>
        

        </body>
        </html>
        '''.format(email=collage.buemail, password=bupassword)

    
        # Create MIMEText object with body and charset
        body_mime = MIMEText(body, 'html', 'utf-8')

        myemail = "442200922@student.ksu.edu.sa"
        # Construct email with headers and body
        email_msg = MIMEMultipart()
        email_msg['Subject'] = subject
        email_msg['From'] = settings.EMAIL_HOST_USER
        email_msg['To'] = myemail
        email_msg.attach(body_mime)

        # Create the SSL context
        context = ssl.create_default_context(cafile=certifi.where())

        # Create connection
        connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        connection.starttls(context=context)

        # Login
        connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Send email
        connection.sendmail(settings.EMAIL_HOST_USER, [myemail], email_msg.as_string())

        # Close connection
        connection.quit()

        print("correctly entered the function")

        return HttpResponse("Password reset email sent.")

def getnationalities():
    nationalitiesList = {
    "Afghan": "أفغاني",
    "Albanian": "ألباني",
    "Algerian": "جزائري",
    "American": "أمريكي",
    "Andorran": "أندوري",
    "Angolan": "أنغولي",
    "Antiguans": "انتيغوا",
    "Argentinean": "أرجنتيني",
    "Armenian": "أرميني",
    "Australian": "أسترالي",
    "Austrian": "نمساوي",
    "Azerbaijani": "أذربيجاني",
    "Bahamian": "باهامى",
    "Bahraini": "بحريني",
    "Bangladeshi": "بنجلاديشي",
    "Barbadian": "باربادوسي",
    "Barbudans": "بربودا",
    "Batswana": "بوتسواني",
    "Belarusian": "بيلاروسي",
    "Belgian": "بلجيكي",
    "Belizean": "بليزي",
    "Beninese": "بنيني",
    "Bhutanese": "بوتاني",
    "Bolivian": "بوليفي",
    "Bosnian": "بوسني",
    "Brazilian": "برازيلي",
    "British": "بريطاني",
    "Bruneian": "بروناى",
    "Bulgarian": "بلغاري",
    "Burkinabe": "بوركيني",
    "Burmese": "بورمي",
    "Burundian": "بوروندي",
    "Cambodian": "كمبودي",
    "Cameroonian": "كاميروني",
    "Canadian": "كندي",
    "Cape Verdean": "االرأس الأخضر",
    "Central African": "وسط أفريقيا",
    "Chadian": "تشادي",
    "Chilean": "شيلي",
    "Chinese": "صينى",
    "Colombian": "كولومبي",
    "Comoran": "جزر القمر",
    "Congolese": "كونغولي",
    "Costa Rican": "كوستاريكي",
    "Croatian": "كرواتية",
    "Cuban": "كوبي",
    "Cypriot": "قبرصي",
    "Czech": "تشيكي",
    "Danish": "دانماركي",
    "Djibouti": "جيبوتي",
    "Dominican": "دومينيكاني",
    "Dutch": "هولندي",
    "East Timorese": "تيموري شرقي",
    "Ecuadorean": "اكوادوري",
    "Egyptian": "مصري",
    "Emirian": "إماراتي",
    "Equatorial Guinean": "غيني  استوائي",
    "Eritrean": "إريتري",
    "Estonian": "إستوني",
    "Ethiopian": "حبشي",
    "Fijian": "فيجي",
    "Filipino": "فلبيني",
    "Finnish": "فنلندي",
    "French": "فرنسي",
    "Gabonese": "جابوني",
    "Gambian": "غامبيي",
    "Georgian": "جورجي",
    "German": "ألماني",
    "Ghanaian": "غاني",
    "Greek": "إغريقي",
    "Grenadian": "جرينادي",
    "Guatemalan": "غواتيمالي",
    "Guinea-Bissauan": "غيني بيساوي",
    "Guinean": "غيني",
    "Guyanese": "جوياني",
    "Haitian": "هايتي",
    "Herzegovinian": "هرسكي",
    "Honduran": "هندوراسي",
    "Hungarian": "هنغاري",
    "Icelander": "إيسلندي",
    "Indian": "هندي",
    "Indonesian": "إندونيسي",
    "Iranian": "إيراني",
    "Iraqi": "عراقي",
    "Irish": "إيرلندي",
    "Italian": "إيطالي",
    "Ivorian": "إفواري",
    "Jamaican": "جامايكي",
    "Japanese": "ياباني",
    "Jordanian": "أردني",
    "Kazakhstani": "كازاخستاني",
    "Kenyan": "كيني",
    "Kittian and Nevisian": "كيتياني ونيفيسياني",
    "Kuwaiti": "كويتي",
    "Kyrgyz": "قيرغيزستان",
    "Laotian": "لاوسي",
    "Latvian": "لاتفي",
    "Lebanese": "لبناني",
    "Liberian": "ليبيري",
    "Libyan": "ليبي",
    "Liechtensteiner": "ليختنشتايني",
    "Lithuanian": "لتواني",
    "Luxembourger": "لكسمبرغي",
    "Macedonian": "مقدوني",
    "Malagasy": "مدغشقري",
    "Malawian": "مالاوى",
    "Malaysian": "ماليزي",
    "Maldivan": "مالديفي",
    "Malian": "مالي",
    "Maltese": "مالطي",
    "Marshallese": "مارشالي",
    "Mauritanian": "موريتاني",
    "Mauritian": "موريشيوسي",
    "Mexican": "مكسيكي",
    "Micronesian": "ميكرونيزي",
    "Moldovan": "مولدوفي",
    "Monacan": "موناكو",
    "Mongolian": "منغولي",
    "Moroccan": "مغربي",
    "Mosotho": "ليسوتو",
    "Motswana": "لتسواني",
    "Mozambican": "موزمبيقي",
    "Namibian": "ناميبي",
    "Nauruan": "ناورو",
    "Nepalese": "نيبالي",
    "New Zealander": "نيوزيلندي",
    "Ni-Vanuatu": "ني فانواتي",
    "Nicaraguan": "نيكاراغوا",
    "Nigerien": "نيجري",
    "North Korean": "كوري شمالي",
    "Northern Irish": "إيرلندي شمالي",
    "Norwegian": "نرويجي",
    "Omani": "عماني",
    "Pakistani": "باكستاني",
    "Palauan": "بالاوي",
    "Palestinian": "فلسطيني",
    "Panamanian": "بنمي",
    "Papua New Guinean": "بابوا غينيا الجديدة",
    "Paraguayan": "باراغواياني",
    "Peruvian": "بيروفي",
    "Polish": "بولندي",
    "Portuguese": "برتغالي",
    "Qatari": "قطري",
    "Romanian": "روماني",
    "Russian": "روسي",
    "Rwandan": "رواندي",
    "Saint Lucian": "لوسياني",
    "Salvadoran": "سلفادوري",
    "Samoan": "ساموايان",
    "San Marinese": "سان مارينيز",
    "Sao Tomean": "ساو توميان",
    "Saudi": "سعودي",
    "Scottish": "سكتلندي",
    "Senegalese": "سنغالي",
    "Serbian": "صربي",
    "Seychellois": "سيشلي",
    "Sierra Leonean": "سيرا ليوني",
    "Singaporean": "سنغافوري",
    "Slovakian": "سلوفاكي",
    "Slovenian": "سلوفيني",
    "Solomon Islander": "جزر سليمان",
    "Somali": "صومالي",
    "South African": "جنوب افريقيي",
    "South Korean": "كوري جنوبي",
    "Spanish": "إسباني",
    "Sri Lankan": "سري لانكي",
    "Sudanese": "سوداني",
    "Surinamer": "سورينامي",
    "Swazi": "سوازي",
    "Swedish": "سويدي",
    "Swiss": "سويسري",
    "Syrian": "سوري",
    "Taiwanese": "تايواني",
    "Tajik": "طاجيكي",
    "Tanzanian": "تنزاني",
    "Thai": "التايلاندي",
    "Togolese": "توغواني",
    "Tongan": "تونجاني",
    "Trinidadian or Tobagonian": "ترينيدادي أو توباغوني",
    "Tunisian": "تونسي",
    "Turkish": "تركي",
    "Tuvaluan": "توفالي",
    "Ugandan": "أوغندي",
    "Ukrainian": "أوكراني",
    "Uruguayan": "أوروجواي",
    "Uzbekistani": "أوزبكستاني",
    "Venezuelan": "فنزويلي",
    "Vietnamese": "فيتنامي",
    "Welsh": "ويلزي",
    "Yemenite": "يمني",
    "Zambian": "زامبي",
    "Zimbabwean": "زيمبابوي"
    }
    nationalities = list(nationalitiesList.values())
    return nationalities