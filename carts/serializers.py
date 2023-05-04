from django.forms import ValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from carts.models import Cart, CartProduct
from products.models import Product
from django.core.validators import MinValueValidator


class CartProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        product_id = validated_data.pop("id_product")
        product = get_object_or_404(Product, pk=product_id)
        amount = product.stock
        if validated_data["amount"] > amount:
            raise ValidationError("Quantity exceed the stock")
        check_product_cart = CartProduct.objects.filter(
            cart=validated_data["cart"].id,
            product=product_id,
        )
        if not check_product_cart:
            return CartProduct.objects.create(**validated_data, product=product)

        final_amount = check_product_cart[0].amount + validated_data["amount"]
        check_product_cart[0].__dict__.update(amount=final_amount)
        check_product_cart[0].save()
        return

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
