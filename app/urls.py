from . import views
from django.urls import include, path

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('addAdmin/', views.addAdmin, name='addAdmin'), 
    path('addSANDF/', views.addSANDF, name='addSANDF'), 
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]