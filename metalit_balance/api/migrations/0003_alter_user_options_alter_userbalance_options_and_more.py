# Generated by Django 4.0.1 on 2022-01-24 14:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_userbalance_account_number_userhistory"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="userbalance",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterField(
            model_name="userhistory",
            name="transaction_id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=255, unique=True
            ),
        ),
        migrations.AddConstraint(
            model_name="userbalance",
            constraint=models.UniqueConstraint(
                fields=("uid", "account_number"), name="unique uid acc_number"
            ),
        ),
    ]
