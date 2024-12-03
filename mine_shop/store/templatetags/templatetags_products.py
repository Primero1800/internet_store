import random
from django.conf import settings
from django import template

from store.models import Product

register = template.Library()

all_products = Product.objects.all()

@register.simple_tag
def add_new_arrivals_to_context():
    """В тестовом варианте для определения новинок применяется вариант с последними опубликованными
        Данные добавляются в БД в хронологическом порядке. Модель Product предполагает упорядочивание по id."""
    new_arrivals = all_products[:settings.PRODUCT_NEW_ARRIVALS_COUNT]
    for_ids = new_arrivals.all().values('id')
    context = {'ids': tuple(v for kv in for_ids for k, v in kv.items())}
    new_arrivals = list(new_arrivals)
    random.shuffle(new_arrivals)
    context['products'] = new_arrivals
    return context

@register.simple_tag
def add_heroes_to_context():
    """В тестовом варианте для определения продуктов-героев применяется вариант с определенным в настройках
        числом продуктов с наибольшей скидкой."""
    heroes = all_products.order_by('-discont')[:settings.PRODUCT_HEROES_COUNT]
    heroes = list(heroes)
    random.shuffle(heroes)
    return heroes



