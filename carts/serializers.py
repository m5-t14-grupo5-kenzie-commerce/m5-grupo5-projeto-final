from django.shortcuts import get_object_or_404
from carts.models import CartProduct
from products.models import Product


class CartSerializer:
    def create(self, validated_data: dict):
        product = get_object_or_404(Product, pk=validated_data["product_id"])
        amount = product["stock"]
        # validar se o amount é maior que 0
        if validated_data["amount"] > amount:
            return "mensagem de erro"
        CartProduct.objects.create(**validated_data)

    class Meta:
        model = CartProduct
        fields = [
            "cart_id",
            "product_id",
            "amount",
        ]
        # depth = 1
        read_only_fields = ["id"]
