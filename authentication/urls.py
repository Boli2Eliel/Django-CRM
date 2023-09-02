# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, users_list, user_update
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('accounts/', users_list, name="accounts"),
    path('user-update/<int:pk>', user_update, name='user-update'),
    path("logout/", LogoutView.as_view(template_name='accounts/logout.html'), name="logout")
]
