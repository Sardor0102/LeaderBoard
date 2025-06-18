from django.contrib.auth.views import LoginView
from django.urls import path

from apps.views import (RegisterCreateAPIView, CustomTokenRefreshView, LogoutAPIView)

urlpatterns = [
    path('register', RegisterCreateAPIView.as_view(), name='register'),
    path('login', CustomTokenRefreshView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
]
