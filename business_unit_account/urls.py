from django.urls import path
from . import views

app_name = 'business_unit_account'

urlpatterns = [
    path('business-unit-home/', views.business_unit_home, name='business_unit_home'),
    path('business-unit-home/profile', views.profile_view, name='profile'),
    path('business-unit-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('business-unit-home/change-password', views.changepassword_view, name='change-password'),
    path('business-unit-home/faculty-list', views.facultylist_view, name='faculty-list'),
    path('business-unit-home/faculty-list/faculty-view/<int:faculty_id>/', views.facultyinfo_view, name='faculty-view'),
    path('business-unit-home/traningprogram', views.traningprogram_view, name='traning-program'),
    path('business-unit-home/profile/view-file/<int:user_id>/', views.view_file, name='view_file'),
    path('business-unit-home/edit-profile/delete_previouswork/<str:value_to_delete>/', views.delete_previouswork, name='delete_previouswork'),
    path('business-unit-home/edit-profile/delete_researchinterest/<str:value_to_delete>/', views.delete_researchinterest, name='delete_researchinterest'),
    path('business-unit-home/edit-profile/delete_course/<int:value_to_delete>/', views.delete_course, name='delete_course'),
   
]
