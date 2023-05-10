from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        name = validated_data["name"]
        saler = validated_data["saler"]
        if Product.objects.filter(name=name, saler=saler).exists():

            raise serializers.ValidationError(
                {"error": "Product already exists!"}
            )

        return Product.objects.create(**validated_data)

    class Meta:
        model = Product
        fields = ["id", "saler_id", "stock", "name", "category", "available", "price"]
