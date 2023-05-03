from django.db import models
import uuid


class CartProduct(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    cart = models.ForeignKey(
        "carts.Cart",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()


class Cart(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    user = models.OneToOneField(
        "users.user",
        on_delete=models.CASCADE,
        related_name="cart",
    )
    products = models.ManyToManyField(
        "products.Product",
        through="CartProduct",
    )
