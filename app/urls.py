from . import views
from django.urls import include, path

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),

    path('Home', views.Home, name='Home'),

    path('client-list', views.client_list, name='client-list'),
    path('client-new', views.client_new, name='client-new'),
    path('client-profile', views.client_profile, name='client-profile'),
    path('client-view', views.client_view, name='client-view'),
    path('index5', views.index5, name='index5'),

    path('index4', views.index4, name='index4'),
    path('project-list', views.project_list, name='project-list'),
    path('project-new', views.project_new, name='project-new'),
    path('project-overclndr', views.project_overclndr, name='project-overclndr'),
    path('project-view', views.project_view, name='project-view'),
    path('edit-profile', views.edit_profile, name='edit-profile'),

    path('empty-page',views.empty_page, name='empty-page'),
    path('forgot-password-1', views.forgot_password_1, name='forgot-password-1'),
    path('login-1', views.login_1, name='login-1'),
    path('profile-1', views.profile_1, name='profile-1'),
    path('reset-password-1', views.reset_password_1, name='reset-password-1'),
    path('settings', views.settings, name='settings'),
    path('chat', views.chat, name='chat'),

]