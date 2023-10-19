from . import views
from django.urls import path, include

app_name = 'faculty_staff_account'

urlpatterns = [ 
    path('faculty-staff-home/', views.faculty_staff_home, name='faculty_staff_home'),
    path('faculty-staff-home/profile', views.profile_view, name='profile'),
    path('faculty-staff-home/edit-profile', views.editprofile_view, name='edit-profile'),
    path('faculty-staff-home/empty-page', views.emptypage_view, name='empty-page'),
    # path('faculty-staff-home/faculty-list', views.facultylist_view, name='faculty-list'),
]
