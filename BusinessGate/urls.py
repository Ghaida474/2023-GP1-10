"""
URL configuration for BusinessGate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('admin-account/', include('admin_account.urls')),
    path('business-unit-account/', include('business_unit_account.urls')),
    path('faculty-staff-account/', include('faculty_staff_account.urls')),
    path('kai_account/', include('kai_account.urls')),
    path('dean/', include('dean.urls')),
    path('kai_staff/', include('kai_staff.urls')),
]
