from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from carts.models import Cart, CartProduct
from carts.serializers import CartProductSerializer
from rest_framework.views import status
from products.models import Product


class CartView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = CartProduct.objects.filter(cart=request.user.cart.id)
        serializer = CartProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class CartProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    lookup_url_kwarg = ["product_id", "cart_id"]

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        cart_product = get_object_or_404(
            CartProduct, cart_id=request.user.cart, product_id=product_id
        )
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *arg, **kwargs):
        product_id = kwargs["product_id"]
        cart_product = get_object_or_404(
            CartProduct, cart_id=request.user.cart, product_id=product_id
        )
        product = get_object_or_404(Product, pk=product_id)
        amount = product.stock

        serializer = CartProductSerializer(
            instance=cart_product, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["amount"] > amount:
            raise ValidationError({"amount": ["Quantity exceeds the stock"]})

        serializer.save()
        return Response(serializer.data)
