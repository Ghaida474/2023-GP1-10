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
    path('faculty-staff-home/traningprogram', views.traningprogram_view, name='traning-program'),
    path('faculty-staff-home/traningprogram/update-status/<int:program_id>/', views.update_status, name='update_status'),
    path('faculty-staff-home/traningprogram/TraningProgram-view/<int:program_id>/', views.program_view, name='program_view'),
    path('faculty-staff-home/traningprogram/view-file/<int:program_id>/', views.view_programfile, name='view_programfile'),
    path('faculty-staff-home/delete_course/<int:value_to_delete>/', views.delete_course, name='delete_course'),
    path('faculty-staff-home/edit_program/<int:value_to_edit>/', views.edit_program, name='edit_program'),
    path('faculty-staff-home/accept-program/<int:id>', views.accept_program, name='accept-program'), 
    path('faculty-staff-home/hasattend/<int:register_id>', views.hasattend, name='hasattend'), 
    path('faculty-staff-home/apply-for-traningprogram/<int:id>/', views.apply_for_traningprogram, name='apply_for_traningprogram'),
    path('faculty-staff-home/reject_program/<int:id>', views.reject_program, name='reject_program'), 



]
    
