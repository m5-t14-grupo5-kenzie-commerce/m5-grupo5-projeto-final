from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    saler = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
    stock = models.IntegerField()
    name = models.CharField(max_length=127)
    category = models.CharField(max_length=127)
    available = models.BooleanField()
    price = models.FloatField(max_length=10, decimal_places=2, null=False)


def __str__(self):
    return f"Product: {self.name} (ID: {self.id})"
