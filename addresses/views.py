from rest_framework import generics
from .serializers import AddressSerializer
from .models import Address
from users.models import User
from .permissions import IsAddressOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
import ipdb


class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressOwner]

    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.kwargs.get("pk"))

    def perform_create(self, serializer) -> None:
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        serializer.save(user=user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressOwner]

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_object(self):
        return Address.objects.get(
            user=self.kwargs.get("pk"), id=self.kwargs.get("pk2")
        )

    def perform_update(self, serializer) -> None:
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        serializer.save(user=user)
