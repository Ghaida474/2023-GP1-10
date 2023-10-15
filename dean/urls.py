from django.urls import path
from . import views

app_name = 'dean_account'

urlpatterns = [
    path('dean-account-home/', views.dean_account_home, name='dean_account_home'),
    path('dean-account-home/profile', views.profile_view, name='profile'),
    # path('dean-account-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('dean-account-home/faculty-list', views.facultylist_view, name='faculty-list'),
     path('dean-account-home/empty-page', views.emptypage_view, name='empty-page'),
]
