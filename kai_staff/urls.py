from django.urls import path
from . import views

app_name = 'kaistaff_account'

urlpatterns = [
    path('kaistaff_home/', views.kaistaff_home, name='kaistaff_home'),
    path('kaistaff_home/profile', views.profile_view, name='profile'),
]
