# Generated by Django 5.1.3 on 2024-12-20 17:14

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0008_cartitem_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
