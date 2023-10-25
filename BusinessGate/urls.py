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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls' , namespace='app')),
    path('admin-account/', include('admin_account.urls')),
    path('business-unit-account/', include('business_unit_account.urls',namespace='business_unit_account')),
    path('faculty-staff-account/', include('faculty_staff_account.urls',namespace='faculty_staff_account')),
    path('headofkai/', include('headofkai.urls',namespace='head-kai-account')),
    path('dean/', include('dean.urls',namespace='dean_account')),
    path('kai-staff/', include('kai_staff.urls', namespace='kai_staff')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#     path('login/', include('app.urls')),  # Include the login URL from app/urls.py
# ]