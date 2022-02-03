# Generated by Django 4.0.1 on 2022-01-27 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_rename_userhistory_usertransactionhistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userbalance",
            name="action",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="userbalance",
            name="uid",
            field=models.OneToOneField(
                db_column="uid",
                on_delete=django.db.models.deletion.CASCADE,
                to="api.user",
                to_field="uid",
            ),
        ),
    ]
