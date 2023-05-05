from rest_framework.serializers import ValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from carts.models import Cart, CartProduct
from products.models import Product
from django.core.validators import MinValueValidator


class CartProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        product = get_object_or_404(Product, pk=validated_data["id_product"])

        amount = product.stock

        if validated_data["amount"] > amount:
            raise ValidationError({"amount": ["Quantity exceeds the stock"]})

        # pega ou cria um item
        # dois primeiros parametros fazem a busca
        # defaults passa o valor caso seja necessario criar
        cart_product, created = CartProduct.objects.get_or_create(
            cart=validated_data["cart"],
            product=product,
            defaults={"amount": validated_data["amount"]},
        )

        # created é um boolean que traz se o true se o objeto foi criado no metodo get_or_create
        #  e false se ele ja existia

        if not created:
            cart_product.amount += validated_data["amount"]
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
