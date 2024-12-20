# Generated by Django 5.1.2 on 2024-11-18 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional_information',
            name='dimensions',
            field=models.CharField(default='Неизвестно', max_length=30, verbose_name='Размер упаковки'),
        ),
        migrations.AlterField(
            model_name='additional_information',
            name='guarantee',
            field=models.CharField(default='Без гарантийных обязательств', max_length=50, verbose_name='Гарантия'),
        ),
        migrations.AlterField(
            model_name='additional_information',
            name='size',
            field=models.CharField(default='Неизвестно', max_length=50, verbose_name='Доп.указания'),
        ),
        migrations.AlterField(
            model_name='additional_information',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=2.0, max_digits=6, verbose_name='Вес в упаковке'),
        ),
        migrations.AlterField(
            model_name='sale_information',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=3, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='sale_information',
            name='sold_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Продажи'),
        ),
        migrations.AlterField(
            model_name='sale_information',
            name='viewed_count',
            field=models.PositiveIntegerField(blank=0, default=0, verbose_name='Просмотры'),
        ),
    ]
