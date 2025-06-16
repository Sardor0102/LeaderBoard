from django.shortcuts import render
from rest_framework.permissions import BasePermission


# Create your views here.
class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "admin":
            return True
        return False