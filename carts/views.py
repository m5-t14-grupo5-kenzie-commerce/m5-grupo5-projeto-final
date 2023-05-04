from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from carts.models import Cart, CartProduct
from carts.serializers import CartProductSerializer
from rest_framework.views import status


class CartView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def list(self, request, *args, **kwargs):
        Cart.objects.filter(id=request.user.cart.id)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class CartProductDetailView(generics.RetrieveUpdateDestroyAPIView):
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
        return Response(status=status.HTTP_204_NO_CONTENT)

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
