# Generated by Django 4.2 on 2023-04-15 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_bookproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookproduct',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bookproduct',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]