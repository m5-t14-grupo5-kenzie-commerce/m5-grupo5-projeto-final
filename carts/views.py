from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from carts.models import Cart, CartProduct
from carts.serializers import CartProductSerializer
from products.models import Product


class CartView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]

    # Verificar se é CartProduct
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def perform_create(self, serializer):
        serializer.save()


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    lookup_url_kwarg = ["product_id", "cart_id"]

    def destroy(self, request, *args, **kwargs):
        cart_id = kwargs["cart_id"]
        product_id = kwargs["product_id"]
        cart_product = get_object_or_404(
            CartProduct, cart_id=cart_id, product_id=product_id
        )
        cart_product.delete()

    def update(self, request, *arg, **kwargs):
        cart_id = kwargs["cart_id"]
        product_id = kwargs["product_id"]
        cart_product = get_object_or_404(
            CartProduct, cart_id=cart_id, product_id=product_id
        )
        serializer = CartProductSerializer(
            instance=cart_product, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
