# Generated by Django 5.1.1 on 2024-09-23 09:16

import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rubric_description_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=store.models.Image.get_image_path, verbose_name='Изображение'),
        ),
    ]
