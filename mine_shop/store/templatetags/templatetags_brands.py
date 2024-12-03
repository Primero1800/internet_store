from django import template

from store.models import Brand

register = template.Library()


@register.simple_tag
def add_brands_to_context():
    brands = Brand.objects.all()
    result = {'all': brands, 'top': {}}
    top_brands = sorted([brand for brand in brands], key=lambda x: x.get_products_count(), reverse=True)[:8]
    result['top'] = top_brands
    return result

@register.simple_tag
def filter_by_brand_title(queryset, brand_title):
    if isinstance(queryset, list):
        return len([1 for prod in queryset if prod.brand.title==brand_title])
    return queryset.filter(brand__title=brand_title).count()

@register.simple_tag
def filter_by_brands(queryset, brands):
    return sorted(set(prod.brand.title for prod in queryset))