from rest_framework import permissions
from .models import Address
from rest_framework.views import View
from rest_framework.views import Request, View
import ipdb


class IsAddressOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Address) -> bool:
        return obj.user == request.user or request.user.is_superuser
