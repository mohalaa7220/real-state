# Generated by Django 4.2 on 2023-04-15 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_bookproduct_created_bookproduct_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookproduct',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]