from django import template
from django.utils.translation import gettext as _
from django.conf import settings
from django.shortcuts import get_object_or_404

import cart
from store.models import Product

register = template.Library()

def _get_product(item):
    if isinstance(item, dict):
        product = get_object_or_404(Product, id=int(item['product_id']))
        return product
    return item.product

@register.filter
def product(item):
    if isinstance(item, dict):
        product = get_object_or_404(Product, id=int(item['product_id']))
        return product
    return item.product

@register.filter
def image(item):
    return _get_product(item).images.first().image.url

@register.filter
def title(item):
    return _get_product(item).title

@register.filter
def delivery_cost(total_price):
    delivery = cart.inner_functions.get_delivery_cost(total_price)
    return str(delivery) + ' ' + settings.CURRENCY if delivery > 0 else _("бесплатно")



