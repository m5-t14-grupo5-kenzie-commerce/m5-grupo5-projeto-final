from rest_framework import serializers
from django.shortcuts import get_object_or_404
from carts.models import CartProduct
from orders.serializers import ReturnProductSerializer
from products.models import Product
from django.core.validators import MinValueValidator
from drf_spectacular.utils import extend_schema_field


class CartProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def create(self, validated_data: dict):
        product = get_object_or_404(Product, pk=validated_data["id_product"])

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

    @extend_schema_field(serializers.IntegerField)
    def get_product(self, obj) -> int:
        product = obj.product
        return ReturnProductSerializer(product).data
