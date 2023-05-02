from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from carts.models import Cart
from carts.serializers import CartSerializer


class CartView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]

    # Verificar se é CartProduct
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save()


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def retrieve(self, request, *args, **kwargs):
        ...

    def destroy(self, request, *args, **kwargs):
        ...
