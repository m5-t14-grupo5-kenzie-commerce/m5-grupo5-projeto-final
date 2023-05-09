from rest_framework import permissions
from .models import Product
from rest_framework.views import View


class IsSalerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_saler


class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Product) -> bool:
        return obj.saler == request.user
