# Generated by Django 4.2 on 2023-10-20 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_is_admin_user_is_guest_remove_user_is_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('guest', 'guest')], default='guest', max_length=5),
        ),
    ]
