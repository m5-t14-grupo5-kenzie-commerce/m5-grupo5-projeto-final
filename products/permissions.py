from rest_framework import permissions
from .models import Product
from rest_framework.views import View


class IsSalerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Product) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.saler_id == request.user
