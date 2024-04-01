from django.urls import path
from . import views

app_name = 'dean_account'

urlpatterns = [
    path('dean-account-home/', views.dean_account_home, name='dean-account-home'),
    path('dean-account-home/change_new_user_password', views.change_new_user_password, name='change_new_user_password'),
    path('dean-account-home/profile', views.profile_view, name='profile'),
    path('dean-account-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('dean-account-home/faculty-list', views.facultylist_view, name='faculty-list'),
    path('dean-account-home/change-password', views.changepassword_view, name='change-password'),
    path('dean-account-home/faculty-list', views.facultylist_view, name='faculty-list'),
    path('dean-account-home/faculty-list/faculty-view/<int:faculty_id>/', views.facultyinfo_view, name='faculty-view'),
    path('dean-account-home/profile/view-file/<int:user_id>/', views.view_file, name='view_file'),
    path('dean-account-home/edit-profile/delete_previouswork/<str:value_to_delete>/', views.delete_previouswork, name='delete_previouswork'),
    path('dean-account-home/edit-profile/delete_researchinterest/<str:value_to_delete>/', views.delete_researchinterest, name='delete_researchinterest'),
    path('dean-account-home/chat', views.chat, name='chat'),
    path('dean-account-home/callsDashboard', views.callsDashboard, name='callsDashboard'),
    path('dean-account-home/videocall', views.videocall, name='videocall'),
    path('dean-account-home/joinroom', views.joinroom, name='joinroom'),
    path('dean-account-home/chat/<str:direct_username>', views.createDirect, name='createDirect'),
]
    