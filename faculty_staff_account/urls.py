from . import views
from django.urls import path, include

app_name = 'faculty_staff_account'

urlpatterns = [ 
    path('faculty-staff-home/', views.faculty_staff_home, name='faculty_staff_home'),
    path('faculty-staff-home/profile', views.profile_view, name='profile'),
    path('faculty-staff-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('faculty-staff-home/empty-page', views.emptypage_view, name='empty-page'),
    path('faculty-staff-home/change-password', views.changepassword_view, name='change-password'),
    path('faculty-staff-home/profile/view-file/<int:user_id>/', views.view_file, name='view_file'),
    path('faculty-staff-home/edit-profile/delete_previouswork/<str:value_to_delete>/', views.delete_previouswork, name='delete_previouswork'),
    path('faculty-staff-home/edit-profile/delete_researchinterest/<str:value_to_delete>/', views.delete_researchinterest, name='delete_researchinterest'),
   
]
    
