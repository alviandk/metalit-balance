# Generated by Django 4.0.1 on 2022-01-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_user_options_alter_userbalance_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userhistory",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="userhistory",
            constraint=models.UniqueConstraint(
                fields=("uid", "account_number", "transaction_id"),
                name="unique uid acc_number trans_id",
            ),
        ),
    ]