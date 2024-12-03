# Generated by Django 5.1.1 on 2024-09-24 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_slug_alter_rubric_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='additional_information',
            options={'verbose_name': 'Дополнительная информация'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterField(
            model_name='additional_information',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=2.0, max_digits=6, verbose_name='Вес изделия в упаковке'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.CreateModel(
            name='Sale_information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold_count', models.PositiveIntegerField(default=0, verbose_name='Количество продаж')),
                ('viewed_count', models.PositiveIntegerField(blank=0, default=0, verbose_name='Количество просмотров позиции')),
                ('voted_count', models.PositiveIntegerField(blank=0, default=0, verbose_name='Количество оценок')),
                ('rating', models.DecimalField(decimal_places=2, default=3, max_digits=3, verbose_name='Рейтинг позиции')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'Информация о движении изделия',
                'verbose_name_plural': 'Информация о движении изделия',
                'ordering': ('viewed_count',),
            },
        ),
    ]