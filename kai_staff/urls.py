from django.urls import path
from . import views

app_name = 'kai_staff'

urlpatterns = [
    path('kaistaff-home/', views.kaistaff_home, name='kaistaff-home'),
    path('kaistaff-home/profile', views.profile_view, name='profile'),
    path('kaistaff-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('kaistaff-home/change-password', views.changepassword_view, name='change-password'),
    path('kaistaff-home/traningprogram', views.traningprogram_view, name='traning-program'),
    path('kaistaff-home/traningprogram/TraningProgram-view/<int:program_id>/', views.program_view, name='program_view'),
    path('kaistaff-home/traningprogram/TraningProgram-view/<int:program_id>/save-certifications/', views.save_certifications, name='save_certifications'),
    path('kaistaff-home/traningprogram/TraningProgram-view/<int:program_id>/save-certifications/<int:trainee_id>/', views.save_certifications, name='save_certifications'),
    path('kaistaff-home/traningprogram/view_certifications/<int:register_id>/', views.view_certifications, name='view_certifications'),
    path('kaistaff-home/traningprogram/delete_certifications/<int:register_id>/', views.delete_certifications, name='delete_certifications'),
    path('kaistaff-home/traningprogram/accept_program/<int:id>/', views.accept_program, name='accept_program'),

    path('kaistaff-home/traningprogram/rejecte_program/<int:id>/', views.rejecte_program, name='rejecte_program'),
    path('kaistaff-home/chat', views.chat, name='chat'),
    path('kaistaff-home/callsDashboard', views.callsDashboard, name='callsDashboard'),
    path('kaistaff-home/videocall', views.videocall, name='videocall'),
    path('kaistaff-home/joinroom', views.joinroom, name='joinroom'),
    path('kaistaff-home/chat/<str:direct_username>', views.createDirect, name='createDirect'),

]
