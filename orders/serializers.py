from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from carts.models import CartProduct
from orders.models import Order, OrderProduct
from products.models import Product
from products.serializers import ProductSerializer
from users.models import User


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


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer

    class Meta:
        model = OrderProduct
        fields = [
            "product",
            "amount",
        ]


class OrderSerializer(serializers.ModelSerializer):
    # product = serializers.SerializerMethodField()
    # products = OrderProductSerializer(many=True, read_only=True)

    def create(self, validated_data: dict):
        # carrinho - product e amount
        user_cart = validated_data["costumer"].cart
        cart = CartProduct.objects.filter(cart=user_cart)
        if not cart:
            raise ValidationError({"error": ["Impossible to order, cart is empty"]})
        # comprador - costumer, que vem através do token
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

        # lista com todos os salers dos produtos que estão no carrinho
        salers = []
        for item in cart:
            if item.product.saler.id not in salers:
                salers.append(item.product.saler.id)

        for saler_id in salers:
            # vendedor - saler, que consigo acessar o vendedor de cada produto através da lista de produtos do carrinho
            saler = User.objects.filter(id=saler_id)

            order = Order.objects.create(
                costumer=costumer,
                saler=saler[0],
            )

            # Filtra, em uma lista, todos os produtos de cart do vendedor atual
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
                current_product.save()
                OrderProduct.objects.create(
                    amount=product.amount,
                    order=order,
                    product=current_product,
                )
        for item in cart:
            item.delete()
        return order

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "product",
            "created_at",
            # "products",
            "amount",
        ]
        read_only_fields = [
            "id",
            "product",
            "created_at",
            "costumer",
            "saler",
            # "products",
            "amount",
        ]
        depth = 1

    # def get_product(self, obj):
    #     product = obj.product.all()
    #     return ReturnProductSerializer(product, many=True).data
