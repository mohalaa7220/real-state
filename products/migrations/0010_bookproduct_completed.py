# Generated by Django 4.2 on 2023-10-12 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_thumbnail_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookproduct',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]