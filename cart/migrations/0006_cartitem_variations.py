# Generated by Django 5.1.3 on 2024-12-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cartitem_variations'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='products.variant'),
        ),
    ]
