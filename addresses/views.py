from rest_framework import generics
from .serializers import AddressSerializer
from .models import Address
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404


class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.kwargs.get("pk"))

    def perform_create(self, serializer) -> None:
        queryset = Address.objects.filter(is_main_address=True).first()
        print(queryset)

        if queryset:
            queryset.is_main_address = False

        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        serializer.save(user=user)
