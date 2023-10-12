from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Admin, FacultyAndStaff, KAI, BusinessUnit
from django.contrib.auth import get_user_model
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




from django.contrib import messages
from .models import Admin

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

        if temp:
            # If you're using Django's built-in authentication system, you can log the user in here.
            # login(request, admin)
            return redirect('app:home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')
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

def home_view(request):
    return render(request, 'home.html')