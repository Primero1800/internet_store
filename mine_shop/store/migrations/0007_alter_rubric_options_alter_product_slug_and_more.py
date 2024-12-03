# Generated by Django 5.1.1 on 2024-09-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_rubrics_rubric_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rubric',
            options={'ordering': ('id',), 'verbose_name': 'Рубрика', 'verbose_name_plural': 'Рубрики'},
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=150, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Наименование'),
        ),
    ]
