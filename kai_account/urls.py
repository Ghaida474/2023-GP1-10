from django.urls import path
from . import views

app_name = 'kai_account'

urlpatterns = [
    path('kai-home/', views.kai_home, name='kai_home'),
    path('kai-home/profile', views.profile_view, name='profile'),
]

