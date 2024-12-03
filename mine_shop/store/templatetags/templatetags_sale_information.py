from django.conf import settings
from django import template
import random

from store.info_classes import Sale_information

register = template.Library()

all_sale_information = Sale_information.objects.all()

@register.simple_tag
def add_top_sales_to_context():
    """"Количество продуктов в категории "Лидеры продаж"  определяется в настройках проекта.
    Данные берутся из таблицы продаж, представленной моделью Sale_information. В категорию бестселлеров попадают лидеры лидеров продаж. """
    raw_top_sales = all_sale_information.order_by('-sold_count')[:settings.PRODUCT_TOP_SALES_COUNT]

    top_sales = [item.product for item in raw_top_sales]
    bestsellers = list(top_sales[:settings.PRODUCT_BESTSELLERS_COUNT])

    context = {}
    context['ids'] = [product.id for product in top_sales]
    context['bids'] = context['ids'][:settings.PRODUCT_BESTSELLERS_COUNT]

    random.shuffle(top_sales)
    random.shuffle(bestsellers)
    context['products'] = top_sales
    context['bestsellers'] = bestsellers
    try :
        context['top_bestseller'] = bestsellers[0]
    except:
        context['top_bestseller'] = None
    return context

@register.simple_tag
def add_top_views_to_context():
    """"Количество продуктов в категории "Лидеры проcмотров"  определяется в настройках проекта.
        Данные берутся из таблицы продаж, представленной моделью Sale_information. """
    top_views = [top.product for top in all_sale_information.order_by('-viewed_count')[:settings.PRODUCT_TOP_VIEWED_COUNT]]
    random.shuffle(top_views)
    return {'products': top_views}

@register.simple_tag
def add_top_rated_to_context():
    top_rated = [top.product for top in all_sale_information.order_by('-viewed_count')[:settings.PRODUCT_TOP_RATED_COUNT]]
    random.shuffle(top_rated)
    return {'products': top_rated}