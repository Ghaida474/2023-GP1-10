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

def home(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to authenticate each user type
        admin = Admin.objects.filter(email=email, password=password).first()
        faculty_staff = FacultyAndStaff.objects.filter(email=email, password=password).first()
        kai = KAI.objects.filter(email=email, password=password).first()
        business_unit = BusinessUnit.objects.filter(email=email, password=password).first()

        # Redirect to the 'home' view of each user type's application if authentication is successful
        if admin:
            return redirect('admin_account:home') # Redirects to the 'home' view of the 'admin_account' application
        elif faculty_staff:
            return redirect('faculty_staff_account:home')  # Redirects to the 'home' view of the 'faculty_staff_account' application
        elif kai:
            return redirect('kai_account:home')  # Redirects to the 'home' view of the 'kai_account' application
        elif business_unit:
            return redirect('business_unit_account:home')  # Redirects to the 'home' view of the 'business_unit_account' application
        else:
            # If authentication fails, show an error message and redirect back to the login page
            messages.error(request, 'Invalid email or password')
            return redirect('app:login')

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
'''from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to authenticate a 'User' type
        User = get_user_model()
        user = User.objects.filter(username=email).first()

        if user is not None and check_password(password, user.password):
            # Check the type of user and redirect to the corresponding home view
            if isinstance(user, FacultyAndStaff):
                return redirect('faculty_staff_account:home')
            elif isinstance(user, KAI):
                return redirect('kai_account:home')
        else:
            # If not a 'User', try with 'Admin' and 'BusinessUnit'
            admin = Admin.objects.filter(email=email).first()
            if admin and admin.password == password:
                return redirect('admin_account:home')

            business_unit = BusinessUnit.objects.filter(email=email).first()
            if business_unit and business_unit.password == password:
                return redirect('business_unit_account:home')

            # If authentication fails, show an error message and redirect back to the login page
            messages.error(request, 'Invalid email or password')
            return redirect('app:login')

    return render(request, 'login.html')'''




'''this is just a temporary function that will be changed later when we change the database'''
'''def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to authenticate a 'User' type
        User = get_user_model()
        user = User.objects.filter(email__startswith=email[0]).first()

        if user is not None and user.password[0] == password[0]:
            # Check the type of user and redirect to the corresponding home view
            if isinstance(user, FacultyAndStaff):
                return redirect('faculty_staff_account:home')
            elif isinstance(user, KAI):
                return redirect('kai_account:home')

        # If not a 'User', try with 'Admin' and 'BusinessUnit'
        admin = Admin.objects.filter(Email__startswith=email[0]).first()
        if admin and admin.Password[0] == password[0]:
            return redirect('admin_account:home')

        business_unit = BusinessUnit.objects.filter(BUemail__startswith=email[0]).first()
        if business_unit and business_unit.Password[0] == password[0]:
            return redirect('business_unit_account:home')

        # If authentication fails, show an error message and redirect back to the login page
        messages.error(request, 'Invalid email or password')
        return redirect('app:login')

    return render(request, 'login.html')'''

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to authenticate a 'User' type
        User = get_user_model()
        user = User.objects.filter(username=email).first()

        if user is not None and user.password == password:
            # Check the type of user and redirect to the corresponding home view
            if user.role == 'faculty_staff':
                return redirect('faculty_staff_account:home')
            elif user.role == 'kai':
                return redirect('kai_account:home')

        # If not a 'User', try with 'Admin' and 'BusinessUnit'
        admin = Admin.objects.filter(email=email).first()
        if admin and admin.password == password:
            return redirect('admin_account:home')

        business_unit = BusinessUnit.objects.filter(email=email).first()
        if business_unit and business_unit.password == password:
            return redirect('business_unit_account:home')

        # If authentication fails, show an error message and redirect back to the login page
        messages.error(request, 'Invalid email or password')
        return redirect('app:login')

    return render(request, 'login.html')
def forgot_password (request): 
    return render(request, 'forgot-password.html')
