# Generated by Django 4.2 on 2023-05-19 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='features',
        ),
        migrations.DeleteModel(
            name='Features',
        ),
    ]