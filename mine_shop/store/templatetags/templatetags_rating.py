from django import template

from store.models import Product

register = template.Library()


@register.filter
def stars_on(rating):
    d = 1
    if not rating:
        rating = 0
    return '1'*rating


@register.filter
def stars_off(rating):
    d = 1
    if not rating:
        rating = 0
    return '1'*(5 - rating)

@register.filter
def get_rating_display(rating):
    for item in Product.RatingChoices.choices:
        if item[0] == rating:
            return item[1]

@register.filter
def verbose_name(the_object, the_field):
    return the_object._meta.get_field(the_field).verbose_name
