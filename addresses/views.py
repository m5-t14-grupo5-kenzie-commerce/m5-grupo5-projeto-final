from rest_framework import generics
from .serializers import AddressSerializer
from .models import Address
from users.models import User
from .permissions import IsAddressOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressOwner]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = Address.objects.filter(user=self.kwargs.get("pk"))
        for item in queryset:
            self.check_object_permissions(self.request, item)
        return queryset

    def perform_create(self, serializer) -> None:
        for item in self.get_queryset():
            self.check_object_permissions(self.request, item)
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        serializer.save(user=user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressOwner]

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_object(self):
        address = Address.objects.get(
            user=self.kwargs.get("pk"), id=self.kwargs.get("pk2")
        )
        self.check_object_permissions(self.request, address)
        return address

    def perform_update(self, serializer) -> None:
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        serializer.save(user=user)
