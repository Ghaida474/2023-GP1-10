from django.urls import path
from . import views

app_name = 'kai_staff'

urlpatterns = [
    path('kaistaff-home/', views.kaistaff_home, name='kaistaff-home'),
    path('kaistaff-home/profile', views.profile_view, name='profile'),
    path('kaistaff-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('kaistaff-home/change-password', views.changepassword_view, name='change-password'),
]
