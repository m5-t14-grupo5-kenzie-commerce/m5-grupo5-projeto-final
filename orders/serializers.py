from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from carts.models import CartProduct
from orders.models import Order
from django.core.validators import MinValueValidator


class OrderSerializer:
    class Meta:
        model = Order
        fields = [
            "costumer",
            "saler",
            "created_at",
            "status",
            "products",
        ]
        # depth = 1
        read_only_fields = [
            "id",
            "created_at",
            "costumer",
            "saler",
        ]
        extra_kwargs = {"amount": {"validators": [MinValueValidator(1)]}}

    def create(self, validated_data: dict):
        product = get_object_or_404(Product, pk=validated_data["product_id"])
        amount = product["stock"]

        if validated_data["amount"] > amount:
            raise ValidationError("Quantity exceed the stock")
        CartProduct.objects.create(**validated_data)
