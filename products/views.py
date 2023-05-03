from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSalerOrReadOnly


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSalerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(saler_id=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSalerOrReadOnly]
