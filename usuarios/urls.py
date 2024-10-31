from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar_usuario'),
    path('solicitante_dashboard/', views.solicitante_dashboard, name='solicitante_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
