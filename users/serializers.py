from rest_framework import serializers
from .models import User
from carts.models import Cart
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        if validated_data["is_admin"]:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        Cart.objects.create(user=user)

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)

        if password:
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_saler",
            "is_admin",
            "is_superuser",
            "cart",
        ]
        read_only_fields = ["id", "cart"]
        # depth = 1

        extra_kwargs = {
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="This field must be unique.",
                    )
                ]
            },
        }
