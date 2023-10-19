from django.urls import path
from . import views

app_name = 'business_unit_account'

urlpatterns = [
    path('business-unit-home/', views.business_unit_home, name='business_unit_home'),
    path('business-unit-home/profile', views.profile_view, name='profile'),
    # path('business-unit-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('business-unit-home/faculty-list', views.facultylist_view, name='faculty-list'),
]
