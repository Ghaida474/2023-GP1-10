from . import views
from django.urls import include, path

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password-to-reset/', views.forgot_password_view, name='forgot-password-to-reset'),
    path('reset-password/<str:email>/<str:role>/', views.reset_password, name='reset_password'),
    path('reset_password_action/<str:email>/<str:role>/', views.reset_password_action, name='reset_password_action'),
]