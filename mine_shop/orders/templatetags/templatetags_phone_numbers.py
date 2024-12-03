from django import template
import django.conf

register = template.Library()

@register.simple_tag
def add_phone_numbers_allowed_regions():
    phone_numbers_regions = django.conf.settings.PHONE_NUMBER_ALOWED_REGIONS
    phone_numbers_default = django.conf.settings.PHONE_NUMBER_DEFAULT_REGION
    return {
            'default_region': phone_numbers_default,
            'allowed_regions': phone_numbers_regions.items(),
    }