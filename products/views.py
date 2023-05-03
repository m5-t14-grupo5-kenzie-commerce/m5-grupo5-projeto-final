from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSalerOrReadOnly


class ProductView(generics.ListCreateAPIView):
    # Inserir JWTAuthentication
    permission_classes = [IsSalerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(saler=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Inserir JWTAuthentication
    permission_classes = [IsSalerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
