from django.db import models


class Product(models.Model):
    saler = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
    stock = models.IntegerField()
    name = models.CharField(max_length=127)
    category = models.CharField(max_length=127)
    available = models.BooleanField()


def __str__(self):
    return f"Product: {self.name} (ID: {self.id})"
