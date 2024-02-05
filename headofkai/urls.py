from django.urls import path
from . import views

app_name = 'head-kai-account'

urlpatterns = [
    path('kai-home/', views.kai_home, name='kai-home'),
    path('kai-home/profile', views.profile_view, name='profile'),
    path('kai-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('kai-home/change-password', views.changepassword_view, name='change-password'),
    path('kai-home/chat', views.chat, name='chat'),
    path('kai-home/callsDashboard', views.callsDashboard, name='callsDashboard'),
    path('kai-home/videocall', views.videocall, name='videocall'),
    path('kai-home/joinroom', views.joinroom, name='joinroom'),

]
