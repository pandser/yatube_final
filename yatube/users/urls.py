from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetDoneView, PasswordChangeDoneView,
    PasswordResetCompleteView
)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup',
    ),
    path(
        'password_reset_form/',
        views.PasswordReset.as_view(),
        name='password_reset_form',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirm.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path(
        'password_change/',
        views.PasswordChange.as_view(),
        name='password_change',
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done',
    ),
]
