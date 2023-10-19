from django.urls import path
from . import views

app_name = 'kai_account'

urlpatterns = [
    path('kai_home/', views.kai_home, name='kai_home'),
    path('kai_home/profile', views.profile_view, name='profile'),
]