from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.CharField(max_length=127, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField(blank=True, null=True)
    is_saler = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<User [{self.id}] - {self.email}>"
