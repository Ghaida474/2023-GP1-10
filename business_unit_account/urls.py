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
    

    path('business-unit-home/edit_program/<int:value_to_edit>/', views.edit_program, name='edit_program'),
    path('business-unit-home/delete_course/<int:value_to_delete>/', views.delete_course, name='delete_course'),
    path('business-unit-home/traningprogram/TraningProgram-view/<int:program_id>/', views.program_view, name='program_view'),

    path('business-unit-home/traningprogram/update-status/<int:program_id>/', views.update_status, name='update_status'),
    path('business-unit-home/traningprogram/view-file/<int:program_id>/', views.view_programfile, name='view_programfile'),
    path('business-unit-home/traningprogram/sendtokai/<int:programid>/', views.sendtokai, name='sendtokai'),
    path('business-unit-home/traningprogram/publish1/<int:program_id>/', views.publish1, name='publish1'),
    path('business-unit-home/paid/<int:register_id>', views.haspaid, name='haspaid'), 
    path('business-unit-home/traningprogram/select_program_team/<int:program_id>/', views.select_program_team, name='select_program_team'),
    path('business-unit-home/traningprogram/send_to_new_trainee/<int:program_id>/<int:instructor_id>/', views.send_to_new_trainee, name='send_to_new_trainee'),
    path('business-unit-home/traningprogram/send_to_new_trainee/<int:program_id>/', views.send_to_new_trainee3, name='send_to_new_trainee3'),
    path('business-unit-home/traningprogram/send_to_new_trainees/<int:program_id>/', views.send_to_new_trainees2, name='send_to_new_trainees2'),

    path('business-unit-home/traningprogram/accepte_facultyprogram/<int:program_id>/', views.accepte_facultyprogram, name='accepte_facultyprogram'),
    path('business-unit-home/traningprogram/rejecte_facultyprogram/<int:program_id>/', views.rejecte_facultyprogram, name='rejecte_facultyprogram'),

    path('business-unit-home/edit_program/deleteWaittingInstructor/<int:id>/', views.deleteWaittingInstructor, name='deleteWaittingInstructor'),

]
