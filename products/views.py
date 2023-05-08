from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsProductOwner, IsSalerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSalerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(saler=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsProductOwner]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductRetrieveNameView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = ["name"]

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.kwargs.get("name"))

    serializer_class = ProductSerializer


class ProductRetrieveCategoryView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = ["category"]

    def get_queryset(self):
        return Product.objects.filter(category__iexact=self.kwargs.get("category"))

    serializer_class = ProductSerializer
