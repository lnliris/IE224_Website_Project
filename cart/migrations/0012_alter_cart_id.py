# Generated by Django 5.1.3 on 2024-12-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0011_alter_cart_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]