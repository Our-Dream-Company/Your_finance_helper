from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='authentication/accept_new_password.html'),
         name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='authentication/password_change_form.html'),
         name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/accept_new_password.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/reser_old_password_and_input_new_form.html'),
         name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_form.html'),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/complete_reset_password.html'),
         name='password_reset_complete'),
]
