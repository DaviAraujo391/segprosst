# usuarios/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='core:home'
    ), name='logout'),

    path('cadastro/', views.cadastro, name='cadastro'),
    path('painel/', views.painel, name='painel'),

    path('senha-esquecida/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset.html',
        email_template_name='usuarios/password_reset_email.html',
        subject_template_name='usuarios/password_reset_subject.txt',
        success_url='/usuarios/senha-enviada/'
    ), name='password_reset'),

    path('senha-enviada/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'
    ), name='password_reset_done'),
]


