from bdb import set_trace
from django.forms import ValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from carts.models import CartProduct
from products.models import Product
from django.core.validators import MinValueValidator


class CartProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        product_id = validated_data.pop("product")

        import ipdb

        ipdb.set_trace()

        print("=" * 100)
        print(product_id)
        print("=" * 100)
        product = get_object_or_404(Product, pk=validated_data["product"])
        amount = product["stock"]

        if validated_data["amount"] > amount:
            raise ValidationError("Quantity exceed the stock")
        CartProduct.objects.create(**validated_data)

    class Meta:
        model = CartProduct
        fields = [
            "cart",
            "product",
            "amount",
        ]
        # depth = 1
        read_only_fields = ["id", "cart"]
        extra_kwargs = {"amount": {"validators": [MinValueValidator(1)]}}
