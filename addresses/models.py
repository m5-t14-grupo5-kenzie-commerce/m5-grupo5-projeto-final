from django.db import models
import uuid


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    street = models.CharField(max_length=127)
    zip_code = models.CharField(max_length=9)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=127, null=True)
    is_main_address = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    def __repr__(self) -> str:
        return f"<User Address [{self.id}] - {self.street}>"
