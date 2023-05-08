from rest_framework.serializers import ValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from carts.models import CartProduct
from orders.serializers import ReturnProductSerializer
from products.models import Product
from django.core.validators import MinValueValidator


class CartProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def create(self, validated_data: dict):
        product = get_object_or_404(Product, pk=validated_data["id_product"])

        amount = product.stock
        # VER SE REALMENTE PRECISA ESSA VERIFICAÇÃO QUANDO FOR ADICIONAR NO CARRINHO
        # fazer a lógica para usar o campo available da products
        # if validated_data["amount"] > amount:
        #     raise ValidationError({"amount": ["Quantity exceeds the stock"]})

        cart_product, created = CartProduct.objects.get_or_create(
            cart=validated_data["cart"],
            product=product,
            defaults={"amount": validated_data["amount"]},
        )

        if not created:
            cart_product.amount = validated_data["amount"]
            cart_product.save()

        return cart_product

    class Meta:
        model = CartProduct
        fields = [
            "product",
            "amount",
            "id_product",
        ]
        read_only_fields = [
            "id",
            "product",
        ]
        extra_kwargs = {
            "amount": {"validators": [MinValueValidator(1)]},
            "id_product": {"write_only": True},
        }
        depth = 1

    def get_product(self, obj):
        product = obj.product
        return ReturnProductSerializer(product).data
