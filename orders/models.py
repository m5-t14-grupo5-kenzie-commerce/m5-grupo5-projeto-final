import uuid
from django.db import models


class OrderStatus(models.TextChoices):
    EM_ANDAMENTO = "Em andamento"
    ENTREGUE = "Entregue"
    DEFAULT = "Pedido realizado"


class OrderProduct(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()


class Order(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    costumer = models.ForeignKey(
        "users.User", related_name="my_orders", on_delete=models.CASCADE
    )
    saler = models.ForeignKey(
        "users.User", related_name="my_sales", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=127, choiches=OrderStatus.choices, default=OrderStatus.DEFAULT
    )
    product = models.ManyToManyField("products.Product", through="OrderProduct")
