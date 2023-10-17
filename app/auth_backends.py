# # app/auth_backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Kaibuemployee, FacultyStaff

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
User = get_user_model()

'''class KaibuemployeeAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None

class FacultyStaffAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None'''

class KaibuemployeeAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Kaibuemployee.objects.get(email=email)
            if user.check_password(password):
                return user
        except Kaibuemployee.DoesNotExist:
            return None 

class FacultyStaffAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = FacultyStaff.objects.get(email=email)
            if user.check_password(password):
                return user
        except FacultyStaff.DoesNotExist:
            return None

'''class AdminAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Your authentication logic for UserType3
        user = Admin.objects.authenticate(email, password)
        return user
'''
