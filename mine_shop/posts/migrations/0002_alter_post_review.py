# Generated by Django 5.1.2 on 2024-11-18 11:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='review',
            field=models.TextField(max_length=500, validators=[django.core.validators.MinLengthValidator(1, 'Не менее одного символа')], verbose_name='Отзыв'),
        ),
    ]
