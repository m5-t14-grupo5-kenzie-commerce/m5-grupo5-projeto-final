# Generated by Django 4.2 on 2023-05-08 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("stock", models.IntegerField()),
                ("name", models.CharField(max_length=127)),
                ("category", models.CharField(max_length=127)),
                ("available", models.BooleanField()),
                (
                    "price",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "saler",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
