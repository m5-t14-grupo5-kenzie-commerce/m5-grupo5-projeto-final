from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from carts.models import CartProduct
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User
from rest_framework.response import Response

from users.serializers import UserSerializer


class ReturnProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "saler_id",
            "name",
            "category",
            "available",
            "price",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "name", "price", "amount", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    costumer = UserSerializer(read_only=True)
    saler = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "costumer", "saler", "status", "items"]
        read_only_fields = ["id", "created_at", "costumer", "saler", "items"]
        depth = 1

    def create(self, validated_data):
        user_cart = validated_data["costumer"].cart
        cart = CartProduct.objects.filter(cart=user_cart)
        if not cart:
            raise ValidationError({"error": ["Impossible to order, cart is empty"]})

        costumer = validated_data["costumer"]

        for item_product in cart:
            if item_product.amount > item_product.product.stock:
                raise ValidationError(
                    {
                        f"{item_product.product.name}": [
                            "Quantity ordered exceeds the stock",
                            f"Quantity in stock: {item_product.product.stock}",
                        ]
                    }
                )

        salers = []
        for item in cart:
            if item.product.saler.id not in salers:
                salers.append(item.product.saler.id)

        for saler_id in salers:
            saler = User.objects.get(id=saler_id)

            order = Order.objects.create(
                costumer=costumer,
                saler=saler,
            )

            saler_products = []
            for item in cart:
                if item.product.saler.id == saler_id:
                    saler_products.append(item)

            for product in saler_products:
                current_product = get_object_or_404(
                    Product,
                    id=product.product_id,
                )
                current_product.stock -= product.amount
                if current_product.stock == 0:
                    current_product.available = False
                current_product.save()

                OrderItem.objects.create(
                    amount=product.amount,
                    order=order,
                    price=current_product.price,
                    name=current_product.name,
                )

        for item in cart:
            item.delete()

        return order
