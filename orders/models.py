import uuid
from django.db import models


class OrderStatus(models.TextChoices):
    EM_ANDAMENTO = "Em andamento"
    ENTREGUE = "Entregue"
    DEFAULT = "Pedido realizado"


class Order(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    costumer = models.ForeignKey(
        "users.User",
        related_name="my_orders",
        on_delete=models.CASCADE,
    )
    saler = models.ForeignKey(
        "users.User",
        related_name="my_sales",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=127,
        choices=OrderStatus.choices,
        default=OrderStatus.DEFAULT,
    )


class OrderItem(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
