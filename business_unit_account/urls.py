from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'business_unit_account'

urlpatterns = [

# 7
    path('business-unit-home/', views.business_unit_home, name='business_unit_home'),
    path('business-unit-home/calendar',views.calendar,name='calendar'),
    
    path('business-unit-home/change_new_user_password', views.change_new_user_password, name='change_new_user_password'),
    path('business-unit-home/profile', views.profile_view, name='profile'),
    path('business-unit-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('business-unit-home/change-password', views.changepassword_view, name='change-password'),
    path('business-unit-home/changeBU-password', views.changeBUpassword_view, name='changeBUpassword_view'),
    path('business-unit-home/profile/view-file/<int:user_id>/', views.view_file, name='view_file'),
    path('business-unit-home/edit-profile/delete_previouswork/<str:value_to_delete>/', views.delete_previouswork, name='delete_previouswork'),
    path('business-unit-home/edit-profile/delete_researchinterest/<str:value_to_delete>/', views.delete_researchinterest, name='delete_researchinterest'),    
# 2
    path('business-unit-home/faculty-list', views.facultylist_view, name='faculty-list'),
    path('business-unit-home/faculty-list/faculty-view/<int:faculty_id>/', views.facultyinfo_view, name='faculty-view'),
# 4
    path('business-unit-home/videocall', views.videocall, name='videocall'),
    path('business-unit-home/joinroom', views.joinroom, name='joinroom'),
    path('business-unit-home/chat', views.chat, name='chat'), 
    path('business-unit-home/projects/groupchat/<int:program_id>/', views.groupchat_view, name='groupchat'),
    path('business-unit-home/chat/<str:direct_username>', views.createDirect, name='createDirect'),
    path('business-unit-home/joinroom_notification', views.joinroom_notification, name='joinroom_notification'),  
    path('business-unit-home/report/<int:program_id>/', views.report, name='report'),
# 16
    path('business-unit-home/traningprogram', views.traningprogram_view, name='traning-program'),
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
# 9
    path('business-unit-home/projects', views.projects_view, name='projects'),
    path('business-unit-home/projects/project-view/<int:program_id>/', views.project_view, name='project_view'),
    path('business-unit-home/edit_project/<int:value_to_edit>/', views.edit_project, name='edit_project'),
    path('business-unit-home/delete_project/<int:value_to_delete>/', views.delete_project, name='delete_project'),
    path('business-unit-home/projects/select_project_team/<int:program_id>/', views.select_project_team, name='select_project_team'),
    path('business-unit-home/projects/send_to_new_member/<int:program_id>/<int:instructor_id>/', views.send_to_new_member, name='send_to_new_member'),
    path('business-unit-home/projects/send_to_new_member/<int:program_id>/', views.send_to_new_member3, name='send_to_new_member3'),
    path('business-unit-home/projects/chooseleader/<int:program_id>/', views.chooseleader, name='chooseleader'),
    path('business-unit-home/projects/SubmittedtoKAI/<int:program_id>/', views.SubmittedtoKAI, name='SubmittedtoKAI'),
    path('business-unit-home/projects/ConfirmDONEproject/<int:program_id>/', views.ConfirmDONEproject, name='ConfirmDONEproject'),
    path('business-unit-home/projects/ConfirmKAI/<int:program_id>/<str:ConfirmKAI>/', views.ConfirmKAI, name='ConfirmKAI'),
    path('business-unit-home/projects/view-file/<int:program_id>/<int:file_id>/', views.view_projectfile, name='view_projectfile'),
    path('business-unit-home/projects/deleteWaittingMember/<int:id>/', views.deleteWaittingMember, name='deleteWaittingMember'),

    path('business-unit-home/tasks', views.task_view, name='tasks'),
    path('business-unit-home/tasks/task_details/<int:task_id>/<int:file_id>/', views.view_tasktfile, name='view_tasktfile'),
    path('business-unit-home/tasks/<int:task_id>/', views.task_details, name='task-detail'),
    path('business-unit-home/tasks/task_details/<int:task_id>/retrieve/', views.retrieve_task, name='retrieve_task'),
    path('business-unit-home/tasks/task_details/<int:task_id>/reject/', views.reject_task, name='reject_task'),
    path('business-unit-home/tasks/task_details/<int:task_id>/Task_completion/', views.Task_completion, name='Task_completion'),
    path('business-unit-home/tasks/task_details/<int:task_id>/ask_for_pending/', views.ask_for_pending, name='ask_for_pending'),
    path('business-unit-home/tasks/task_details/<int:task_id>/accepte_pending_request/', views.accepte_pending_request, name='accepte_pending_request'),
    path('business-unit-home/tasks/task_details/<int:task_id>/reject_pending_request/', views.reject_pending_request, name='reject_pending_request'),
    path('business-unit-home/tasks/task_details/<int:task_id>/editTask/', views.editTask, name='editTask'),
    path('business-unit-home/tasks/task_details/<int:task_id>/send_to_new_Instructor/', views.send_to_new_Instructor, name='send_to_new_Instructor'),


    path('business-unit-home/email_notification_settings', views.email_notification_settings, name='email_notification_settings'),
    path('business-unit-home/read_notification', views.update_notifications_ajax, name='read_notification'),
    path('business-unit-home/Delete_notification/<int:notification_id>', views.update_notifications_ajax_Delete, name='Delete_notification'),

    path('business-unit-home/report/<int:program_id>/', views.report, name='report'),
    path('business-unit-home/report2/<int:program_id>/', views.report2, name='report2'),
]
urlpatterns += staticfiles_urlpatterns()