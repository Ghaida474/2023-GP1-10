from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import check_password, make_password 
from django.shortcuts import render, redirect
from .forms import Loginform 
from .models import Admin, FacultyStaff, Kaibuemployee,Collage
from django.conf import settings
import random
import string
import smtplib
import ssl
from datetime import datetime, timedelta
from django.http import HttpResponse
from .forms import emailcheckform
import certifi
from django.utils import timezone
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

def index(request): 
    return render(request, 'auth/index.html')

def login_view(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()  
            password = form.cleaned_data.get('password')
           
            if Collage.objects.filter(buemail=email).exists():
                bu = Collage.objects.get(buemail=email)
                if check_password(password, bu.password):
                    if FacultyStaff.objects.filter(is_buhead=True, collageid=bu).exists():
                        buuser = FacultyStaff.objects.get(is_buhead=True, collageid=bu)
                        user = authenticate(request, email=buuser.email, password=buuser.password ,backend='buAuthBackend')
                        login(request, user)
                        return redirect('business_unit_account:business_unit_home')
                    else:
                        clear_messages(request)
                        messages.error(request, 'لا يوجد رئيس وحدة اعمال في هذه الكلية في النظام')
                else:
                    clear_messages(request)
                    messages.error(request, 'كلمة السر غير صحيحة.')
         

            elif FacultyStaff.objects.filter(email=email).exists():
                if authenticate(request, email=email, password=password):
                    user = authenticate(request, email=email, password=password)
                    login(request, user)
                    faculty = FacultyStaff.objects.get(email=email)
                    if faculty.position == 'عميد الكلية':
                        return redirect('dean_account:dean-account-home')
                    elif faculty.position == 'عضو هيئة التدريس' or faculty.position == 'موظف في الكلية':
                        return redirect('faculty_staff_account:faculty_staff_home')
                else:
                    clear_messages(request)
                    messages.error(request, 'كلمة السر غير صحيحة.')
   

            elif Kaibuemployee.objects.filter(email=email).exists():
                if authenticate(request, email=email, password=password):
                    user = authenticate(request, email=email, password=password)
                    login(request, user)
                    kai = Kaibuemployee.objects.get(email=email)
                    if kai.position == 'رئيس قسم وحدات الأعمال بمعهد الملك عبدالله':
                        print('head')
                        return redirect('head-kai-account:kai-home')
                    elif kai.is_department_head:
                        print('department head')
                        return redirect('head-kai-account:kai-home')   
                    else:
                        print('staff')
                        return redirect('kai_staff:kaistaff-home')  
                else:
                    clear_messages(request)
                    messages.error(request, 'كلمة السر غير صحيحة.')


            elif Admin.objects.filter(email=email).exists():
                if authenticate(request, email=email, password=password):
                    user = authenticate(request, email=email, password=password)
                    login(request, user)
                    return redirect('admin_account:admin_home')  
                else:
                    clear_messages(request)
                    messages.error(request, 'كلمة السر غير صحيحة.')
                
            else:
                clear_messages(request)
                messages.error(request, 'البريد الإلكتروني غير صحيح.')
        else:
            clear_messages(request)
            messages.error(request,'خطأ ما حصل وقت الارسال حاول تسجيل الدخول مره آخرى')
            form = Loginform()
            return render(request, 'auth/login.html', {'form': form })
    else:
        form = Loginform()
    return render(request, 'auth/login.html', {'form': form })

def forgot_password_view(request):
    
    if request.method == 'POST':
        form = emailcheckform(request.POST)
        print("Form errors before validation:", form.errors) 
        if form.is_valid():
            email = form.cleaned_data['email']

            if Kaibuemployee.objects.filter(email=email).exists() or FacultyStaff.objects.filter(email=email).exists() or Collage.objects.filter(buemail=email).exists() or Admin.objects.filter(email=email).exists():
                print("User's credentials check")
                send_email_to_reset_password(request, email)
                return redirect('app:reset_password', email=email)
            else:
                clear_messages(request)
                messages.error(request, ' البريد الإلكتروني غير صحيح.')
        
    form = emailcheckform()
    return render(request, 'auth/forgot-password.html', {'form': form})

def send_email_to_reset_password(request, email):
    context = {
        'email': email,
    }
    print("send email function entered successfully")
    print("receiver email", email)

    # Generate a 6-digit OTP
    otp = ''.join(random.choice(string.digits) for _ in range(6))
    print(otp)

    # Construct the email message
    subject = 'كلمة المرور لمرة واحدة (OTP) لإعادة تعيين كلمة المرور'

    body = '''\
        <html>
        <body>
        <p align="right" dir="rtl">السلام عليكم،</p>

        <p align="right" dir="rtl">.لقد طلبت إعادة تعيين كلمة المرور. كلمة المرور لمرة واحدة (OTP) الخاصة بك هي: {otp}</p>

        <p align="right" dir="rtl">هذه الكلمة صالحة لمدة ١٠ دقائق فقط. إذا انتهت صلاحية الكلمة قبل إعادة تعيين كلمة المرور الخاصة بك، يرجى التوجه إلى صفحة تسجيل الدخول لإنشاء كلمة مرور جديدة لمرة واحدة (OTP).</p>

        <p align="right" dir="rtl">شكرا لك،<br>فريق الدعم الخاص بوابة الأعمال</p>

        </body>
        </html>
        '''.format(otp=otp)


    myemail = "442200922@student.ksu.edu.sa"
    # Create MIMEText object with body and charset
    body_mime = MIMEText(body, 'html', 'utf-8')

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

    # Store OTP and the current timestamp in session
    request.session['otp'] = otp
    request.session['otp_timestamp'] = str(timezone.now())

    return HttpResponse("Password reset email sent.")

def reset_password(request, email):
    context = {'email': email}
    return render(request, 'auth/reset-password.html', context)

def reset_password_action(request, email):
    # Retrieve password and otp from post data
    entered_otp = request.POST.get('otp')
    new_password = request.POST.get('new_password')

    # Retrieve OTP and its timestamp from session
    session_otp = request.session.get('otp')
    otp_timestamp_str = request.session.get('otp_timestamp')

    # Remove ":" from the timezone offset
    otp_timestamp_str = otp_timestamp_str.replace("+00:00", "+0000")

    # Now parse the timestamp
    otp_timestamp = datetime.strptime(otp_timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

    if timezone.now() - otp_timestamp > timedelta(minutes=10):
        # OTP expired, delete it from session
        del request.session['otp']
        del request.session['otp_timestamp']

        # Send a new OTP
        send_email_to_reset_password(request, email)

        # Show a message for expired OTP
        clear_messages(request)
        messages.error(request, 'انتهت صلاحية كلمة المرور لمرة واحدة(OTP)، وتم إرسال كلمة مرور لمرة واحدة جديدة إلى بريدك الإلكتروني.')
        return reset_password(request, email)
    else:
        # OTP not expired
        if entered_otp != session_otp:
            # Entered OTP does not match the one in session
            del request.session['otp']
            del request.session['otp_timestamp']

            # Send a new OTP
            send_email_to_reset_password(request, email)

            # Show a message for incorrect OTP
            clear_messages(request)
            messages.error(request, 'كلمة مرور لمرة واحدة غير صحيحة(OTP)، تم إرسال كلمة مرور لمرة واحدة جديدة إلى بريدك الإلكتروني.')
            return reset_password(request, email)
        else:
            # OTP matches, delete it from session
            del request.session['otp']
            del request.session['otp_timestamp']

            # Handle different roles
            if Collage.objects.filter(buemail=email).exists():
                bu = Collage.objects.get(buemail=email)
                bu.password = make_password(new_password)
                bu.save()
            elif FacultyStaff.objects.filter(email=email).exists(): 
                user = FacultyStaff.objects.get(email=email)
                user.set_password(new_password)
                user.save()
            elif Kaibuemployee.objects.filter(email=email).exists(): 
                user = Kaibuemployee.objects.get(email=email)
                user.set_password(new_password)
                user.save()
            elif Admin.objects.filter(email=email).exists():
                user = Admin.objects.get(email=email)
                user.set_password(new_password)
                user.save()
           
            # Show a message for successful password reset
            clear_messages(request)
            messages.error(request, 'تم إعادة تعيين كلمة المرور بنجاح.')
            return redirect('app:login')
            # Show a message for incorrect OTP

@login_required
def logout_view(request):
    # user = request.user
    logout(request)
    clear_messages(request)
    messages.error(request, 'لقد تم تسجيل خروجك بنجاح.')
    response = HttpResponse()
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return redirect('app:login')