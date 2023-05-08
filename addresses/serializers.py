from rest_framework import serializers
from .models import Address
from users.models import User
from django.shortcuts import get_object_or_404
import ipdb


class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Address:
        true_addresses = Address.objects.filter(is_main_address=True)
        user_true_address = true_addresses.filter(user=validated_data.get("user"))

        if validated_data["is_main_address"]:
            if user_true_address:
                for item in user_true_address:
                    # ipdb.set_trace()
                    item.is_main_address = False

            Address.objects.save(**user_true_address)

        return Address.objects.create(**validated_data)

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
