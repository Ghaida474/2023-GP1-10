# # app/auth_backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Kaibuemployee, FacultyStaff, Collage, Admin
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import get_user_model
User = get_user_model()



class KaibuemployeeAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Kaibuemployee.objects.get(email__iexact=email)
            if user.check_password(password):
                print(f"User '{user.email}' authenticated successfully.")
                return user
        except Kaibuemployee.DoesNotExist:
            print(f"User with email '{email}' does not exist.")
        return None

class FacultyStaffAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = FacultyStaff.objects.get(email__iexact=email)
            if user.check_password(password):
                print(user)
                return user
        except FacultyStaff.DoesNotExist:
            return None






