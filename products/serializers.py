from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        fields = ["id", "saler_id", "stock", "name", "category", "available", "price"]
