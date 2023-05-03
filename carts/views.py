from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from carts.models import Cart, CartProduct
from carts.serializers import CartSerializer
from products.models import Product


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

    # def update(self, request, *args, **kwargs):
    #     ...

    def destroy(self, request, *args, **kwargs):
        cart_id = kwargs["pk"]
        product_id = kwargs["product_id"]
        cart_product = get_object_or_404(
            CartProduct, cart_id=cart_id, product_id=product_id
        )
        cart_product.delete()

    def update(self, request, *arg, **kwargs):
        cart_id = kwargs["pk"]
        product_id = kwargs["product_id"]
        cart_product = get_object_or_404(
            CartProduct, cart_id=cart_id, product_id=product_id
        )
        serializer = CartSerializer(instance=cart_product, data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, pk=product_id)
        amount = product["stock"]
        if request.data["amount"] > amount:
            return "mensagem de erro"
        if request.data["amount"] > 0:
            return "outra mensagem de erro"
        serializer.save()
        return Response(serializer.data)
