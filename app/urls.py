from . import views
from django.urls import include, path

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('Home', views.Home, name='Home'),
    path('faculty-list', views.facultylist, name='faculty-list'),
    path('faculty-view', views.facultyview, name='faculty-view'),
    path('project-list', views.project_list, name='project-list'),
    path('project-new', views.project_new, name='project-new'),
    path('project-overclndr', views.project_overclndr, name='project-overclndr'),
    path('project-view', views.project_view, name='project-view'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('empty-page',views.empty_page, name='empty-page'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('settings', views.settings, name='settings'),
    path('chat', views.chat, name='chat'),

]