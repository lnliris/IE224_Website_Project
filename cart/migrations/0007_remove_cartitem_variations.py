# Generated by Django 5.1.3 on 2024-12-22 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_cartitem_variations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
    ]