from django.urls import path
from django.urls.base import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='authentication/accept_new_password.html'),
         name='accept_new_password'),
    path('password_change_form/', auth_views.PasswordChangeView.as_view(template_name='authentication/password_change_form.html', success_url=reverse_lazy('accept_new_password')),
         name='password_change_form'),
    path('password_reset_form/',
         auth_views.PasswordResetView.as_view(
             template_name='authentication/password_reset_form.html',
             subject_template_name='authentication/password_reset_subject.txt',
             success_url=reverse_lazy('accept_reset_password')),
         name='password_reset_form'),
    path('accept_reset_password/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='authentication/accept_reset_password.html'),
         name='accept_reset_password'),
    path('password_reset_<uidb64>_<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='authentication/reset_old_password_and_input_new_form.html',
             success_url=reverse_lazy('complete_reset_password')),
         name='password_reset_confirm'),
    path('complete_reset_password/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='authentication/complete_reset_password.html'),
         name='complete_reset_password'),
]
