from django.urls import path
from . import views

app_name = 'admin_account'

urlpatterns = [
  
    path('admin-home/', views.admin_home, name='admin_home'),
    path('admin-home/addFaculty/', views.addFaculty, name='addFaculty'),
    path('admin-home/facultyList/', views.facultyList, name='facultyList'),
    path('admin-home/editfaculty/<int:id>', views.editfaculty, name='editfaculty'),
    path('admin-home/deletefaculty/<int:id>', views.deletefaculty, name='deletefaculty'),
    
    path('admin-home/addKai/', views.addKai, name='addKai'),
    path('admin-home/kaiList/', views.kaiList, name='kaiList'),
    path('admin-home/editkai/<int:id>', views.editkai, name='editkai'),
    path('admin-home/deletekai/<int:id>', views.deletekai, name='deletekai'),

    path('admin-home/addCollage/', views.addCollage, name='addCollage'),
    path('admin-home/collageList/', views.collageList, name='collageList'),
    path('admin-home/editcollage/<int:id>', views.editcollage, name='editcollage'),
    path('admin-home/deletecollage/<int:id>', views.deletecollage, name='deletecollage'),
    path('admin-home/checkdepartment/<str:department>', views.checkdepartment, name='checkdepartment'),
    path('admin-home/checkdomain/<str:domain>', views.checkdomain, name='checkdomain'),
    
    path('admin-home/checkBU/<int:collage_id>', views.checkBU, name='checkBU'),
    path('admin-home/checkEmail/<str:email>', views.checkEmail, name='checkEmail'),
    path('admin-home/checkposition/', views.checkposition, name='checkposition'),
    path('admin-home/checkDean/', views.checkDean, name='checkDean'),
    
    
]
