# Generated by Django 5.1.1 on 2024-10-23 13:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_usertools_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertools',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
    ]
