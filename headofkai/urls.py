from django.urls import path
from . import views

app_name = 'head-kai-account'

# head-kai-account:kai-home
urlpatterns = [
    path('kai-home/', views.kai_home, name='kai-home'),
    path('kai-home/change_new_user_password', views.change_new_user_password, name='change_new_user_password'),
    path('kai-home/profile', views.profile_view, name='profile'),
    path('kai-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('kai-home/change-password', views.changepassword_view, name='change-password'),
    path('kai-home/chat', views.chat, name='chat'),
    path('kai-home/videocall', views.videocall, name='videocall'),
    path('kai-home/joinroom', views.joinroom, name='joinroom'),
    path('kai-home/chat/<str:direct_username>', views.createDirect, name='createDirect'),

    path('kai-home/tasks', views.task_view, name='tasks'),
    path('kai-home/tasks/task_details/<int:task_id>/<int:file_id>/', views.view_tasktfile, name='view_tasktfile'),
    path('kai-home/tasks/<int:task_id>/', views.task_details, name='task-detail'),
    path('kai-home/tasks/task_details/<int:task_id>/retrieve/', views.retrieve_task, name='retrieve_task'),
    path('kai-home/tasks/task_details/<int:task_id>/reject/', views.reject_task, name='reject_task'),
    path('kai-home/tasks/task_details/<int:task_id>/Task_completion/', views.Task_completion, name='Task_completion'),
    path('kai-home/tasks/task_details/<int:task_id>/ask_for_pending/', views.ask_for_pending, name='ask_for_pending'),
    path('kai-home/tasks/task_details/<int:task_id>/accepte_pending_request/', views.accepte_pending_request, name='accepte_pending_request'),
    path('kai-home/tasks/task_details/<int:task_id>/reject_pending_request/', views.reject_pending_request, name='reject_pending_request'),
    path('kai-home/tasks/task_details/<int:task_id>/editTask/', views.editTask, name='editTask'),
    path('kai-home/tasks/task_details/<int:task_id>/send_to_new_Instructor/', views.send_to_new_Instructor, name='send_to_new_Instructor'),

    path('kai-home/email_notification_settings', views.email_notification_settings, name='email_notification_settings'),
    path('kai-home/read_notification', views.update_notifications_ajax, name='read_notification'),
    path('kai-home/Delete_notification/<int:notification_id>', views.update_notifications_ajax_Delete, name='Delete_notification'),
]
