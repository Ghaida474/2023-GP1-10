from django.urls import path
from . import views

app_name = 'kai_account'

urlpatterns = [
    path('kai-home/', views.kai_home, name='kai-home'),
    path('kai-home/profile', views.profile_view, name='profile'),
    path('kai-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('kai-home/change-password', views.changepassword_view, name='change-password'),

]
