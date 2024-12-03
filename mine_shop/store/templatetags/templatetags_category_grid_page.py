from django import template

register = template.Library()

@register.filter
def listed(queryset):
    result = list(queryset) if not isinstance(queryset, list) else queryset
    return result

@register.filter
def ids(queryset):
    return [product.id for product in queryset]



