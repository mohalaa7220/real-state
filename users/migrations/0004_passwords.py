# Generated by Django 4.2 on 2023-10-20 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passwords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=220)),
            ],
        ),
    ]
