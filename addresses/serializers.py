from rest_framework import serializers
from .models import Address
from users.models import User
from django.shortcuts import get_object_or_404
import ipdb


class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Address:
        true_addresses = Address.objects.filter(
            is_main_address=True, user=validated_data.get("user")
        )

        if validated_data["is_main_address"]:
            if true_addresses:
                for item in true_addresses:
                    item.is_main_address = False
                    item.save()

        return Address.objects.create(**validated_data)

    def update(self, instance: Address, validated_data: dict) -> Address:
        true_addresses = Address.objects.filter(
            is_main_address=True, user=validated_data.get("user")
        )

        if validated_data["is_main_address"]:
            if true_addresses:
                for item in true_addresses:
                    item.is_main_address = False
                    item.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "zip_code",
            "number",
            "complement",
            "user_id",
            "is_main_address",
        ]

        extra_kwargs = {"user_id": {"read_only": True}}
