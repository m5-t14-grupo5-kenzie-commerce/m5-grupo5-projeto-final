from rest_framework import permissions
from .models import User
from rest_framework.views import View
from rest_framework.views import Request, View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        return obj == request.user or request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        if request.method == "GET":
            return obj == request.user or request.user.is_superuser
