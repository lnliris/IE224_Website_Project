# Generated by Django 5.1.3 on 2024-12-16 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_category_slug_product_slug_variant"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_1",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
        migrations.AddField(
            model_name="product",
            name="image_2",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
        migrations.AddField(
            model_name="product",
            name="image_3",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]
