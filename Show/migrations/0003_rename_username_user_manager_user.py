# Generated by Django 4.2.9 on 2024-01-28 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Show', '0002_alter_user_manager_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_manager',
            old_name='username',
            new_name='user',
        ),
    ]
