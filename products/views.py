from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSalerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSalerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(saler=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSalerOrReadOnly]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
