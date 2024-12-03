# Generated by Django 5.1.1 on 2024-09-20 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименование')),
                ('slug', models.SlugField(default='', unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('start_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Начальная цена')),
                ('discont', models.PositiveIntegerField(choices=[(0, 'no discont'), (5, '5% discont'), (10, '10% discont'), (15, '15% discont'), (20, '20% discont'), (25, '25% discont'), (30, '30% discont'), (35, '35% discont'), (40, '40% discont'), (45, '45% discont'), (50, '50% discont'), (55, '55% discont'), (60, '60% discont'), (65, '65% discont'), (70, '70% discont')], default=0, verbose_name='Скидка')),
                ('rating', models.PositiveIntegerField(choices=[(0, 'Нет голосов'), (1, 'Ужасно'), (2, 'Плохо'), (3, 'Средне'), (4, 'Хорошо'), (5, 'Отлично')], default=0, verbose_name='Рейтинг изделия')),
                ('available', models.CharField(max_length=50, choices=[('0', 'в продаже'), ('1', 'нет в наличии')], default=('0', 'в продаже'))),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.brand', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукция',
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/<django.db.models.fields.related.ForeignKey>/', verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Additional_information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=6, verbose_name='Вес изделия в упаковке')),
                ('dimensions', models.CharField(default='Неизвестно', max_length=30, verbose_name='Размер упаковки в сантиметрах')),
                ('size', models.CharField(default='Неизвестно', max_length=50, verbose_name='Указания о размере изделия')),
                ('guarantee', models.CharField(default='Без гарантийных обязательств', max_length=50, verbose_name='Указания о гарантии')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
