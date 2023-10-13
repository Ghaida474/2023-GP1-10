from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from .models import Admin,User,FacultyAndStaff,Businessunit,Kai,Collage,Program,Project,Register,Request,Trainee,Trainingprogram
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from .forms import adminform ,FASform,Loginform


def index(request):
    # This view renders the 'index.html' for the main app.
    return render(request, 'index.html')

def login(request):
    # This view renders the login page.
    return render(request, 'login.html')


''''
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to authenticate a 'User' type
        User = get_user_model()
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check the type of user and redirect to the corresponding home view
            if isinstance(user, FacultyAndStaff):
                return redirect('faculty_staff_account:home')
            elif isinstance(user, KAI):
                return redirect('kai_account:home')
        else:
            # If not a 'User', try with 'Admin' and 'BusinessUnit'
            admin = Admin.objects.filter(email=email).first()
            if admin and check_password(password, admin.password):
                return redirect('admin_account:home')

            business_unit = BusinessUnit.objects.filter(email=email).first()
            if business_unit and check_password(password, business_unit.password):
                return redirect('business_unit_account:home')

            # If authentication fails, show an error message and redirect back to the login page
            messages.error(request, 'Invalid email or password')
            return redirect('app:login')
            

    return render(request, 'login.html')
    '''


def forgot_password(request):
    return redirect('app:index')
    # Your code here

# هنا
'''def login_view(request):

    form = loginform(request.POST or None)
    if request.method == 'POST':
        email1 = request.POST.get('email')
        password1 = request.POST.get('password')
        print('Input Email:', email1)
        print('Input Password:', password1)
        temp = False

        admins = Admin.objects.all()
        print('Number of Admins:', admins.count())  # Print the number of Admin objects

        for admin in admins:
            email = admin.email
            password = admin.password
            print('Admin Email:', email)
            print('Admin Password:', password)

            if email == email1 and password == password1:
                temp = True
                break

        if temp:
            # If you're using Django's built-in authentication system, you can log the user in here.
            # login(request, admin)
            return redirect('app:index')
        else:
            messages.error(request, 'Invalid credentials.')

        return render(request, 'login.html' ,{'form': form})
'''


'''
def login_view(request):
    if request.method == 'POST':
        email1 = request.POST.get('email')
        password1 = request.POST.get('password')
        print('Input Email:', email1)
        print('Input Password:', password1)
        temp = False

        admins = Admin.objects.all()
        print('Number of Admins:', admins.count())  # Print the number of Admin objects
        for admin in admins:
            email = admin.email
            password = admin.password
            print('Admin Email:', email)
            print('Admin Password:', password)

            if email == email1 and password == password1:
                temp = True
                break
        if temp == False
            faculty_staff_members = FacultyAndStaff.objects.all()
            print('Number of Faculty and Staff:', faculty_staff_members.count())  # Print the number of FacultyAndStaff objects
            for member in faculty_staff_members:
                email = member.email
                passwordm = member.password
                print('Faculty/Staff Email:', email)
                print('Faculty/Staff Password:', password)

                if email == email1 and password == password1:
                    temp = True
                    break
        if temp==False
            kai_members = KAI.objects.all()
            print('Number of KAI:', kai_members.count())  # Print the number of KAI objects
            for member in kai_members:
                email = member.email
                password = member.password
                print('KAI Email:', email)
                print('KAI Password:', password)

                if email == email1 and password == password1:
                    temp = True
                    break
        if temp==False        
            business_units = BusinessUnit.objects.all()
            print('Number of Business Units:', business_units.count())  # Print the number of BusinessUnit objects
            for unit in business_units:
                email = unit.email
        # No password field exists in BusinessUnit model
    print('Business Unit Email:', email)

    if email == email1:
        temp = True
        break
    
        
    return render(request, 'login.html')'''


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

    return render(request, 'add-admin.html', {'form1': form1})

  
            
def addSANDF (request):
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
    return render(request, 'add-SANDF.html', {'form2': form2})


def login_view(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            
            if role == 'admin':
                # Check if the user is an admin
                if Admin.objects.filter(email=email).exists():
                    admin = Admin.objects.get(email=email)
                    if check_password(password, admin.password):
                        # login(request, admin)
                        return redirect('app:index') 
                    else:
                        messages.error(request, 'Invalid password.')
                else:
                    messages.error(request, 'This email does not exist.')

            elif role == 'BU' or role == 'dean' or role =='facultyandstaff' :
  
                if FacultyAndStaff.objects.filter(email=email).exists():
                    staff = FacultyAndStaff.objects.get(email=email)
                    if check_password(password, staff.password):
                        return redirect('app:index')
                    else:
                        messages.error(request, 'Invalid password.')
                else:
                    messages.error(request, 'This email does not exist.')
                
            elif role == 'Hkai' or role == 'kaistaff' :
                if Kai.objects.filter(email=email).exists():
                    KAI = Kai.objects.get(email=email)
                    if check_password(password, KAI.password):
                        return redirect('app:index')
                    else:
                        messages.error(request, 'Invalid password.')
                else:
                    messages.error(request, 'This email does not exist.')
            else:
                messages.error(request, 'Invalid role.')
        else:
            messages.error(request, 'Form is invalid. Please check your input.')

    else:
        form = Loginform()

    return render(request, 'login.html', {'form': form})


def home (request):
    return render(request, 'Home.html')