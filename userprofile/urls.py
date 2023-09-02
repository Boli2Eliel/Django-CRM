from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from userprofile import views

# User
urlpatterns = [

    path('success/', views.success, name="success"),
    path('profile_details/', views.profile_details, name='user-profile-details'),
    #path('profile_add/', views.profile_add, name='user-profile-add'),
    path('profile/update/', views.profile_update, name='user-profile-update'),

    # ResetPassword
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),
         name='password_reset'),

    # ResetPasswordDone
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
         name='password_reset_done'),

    # ResetPasswordConfirm
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),  # -->uidb64 and 'token' are sourced from the confirmview error by django admin

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html'), name="password_change"),

    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name="password_change_done"),

    #path('register/', views.register, name="user-register"),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),

]
