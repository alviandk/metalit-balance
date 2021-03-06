# Generated by Django 4.0.1 on 2022-01-19 04:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="UserBalance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("balance", models.BigIntegerField(default=0)),
                ("action", models.CharField(blank=True, default=None, max_length=255)),
                (
                    "uid",
                    models.ForeignKey(
                        db_column="uid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.user",
                        to_field="uid",
                    ),
                ),
            ],
        ),
    ]
