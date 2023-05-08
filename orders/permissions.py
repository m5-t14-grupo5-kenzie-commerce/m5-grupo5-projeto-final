from rest_framework import permissions
from rest_framework.views import View
from orders.models import Order


class IsSaler(permissions.BasePermission):
    def has_permission(self, request, view: View):
        if request.method == "POST" and request.user.is_authenticated:
            return True
        if (
            request.method in permissions.SAFE_METHODS
            and request.user.is_saler
            and request.user.is_authenticated
        ):
            return True


# Permissão não está funcionando corretamente
class IsOrderSaler(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Order):
        if request.method == "PATCH":
            return obj.saler == request.user
        else:
            return True
