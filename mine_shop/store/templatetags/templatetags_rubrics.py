import random

from django import template

from store.models import Rubric

register = template.Library()

rubrics = Rubric.objects.all()

@register.simple_tag
def add_rubrics_to_context():
    return {'all': rubrics}

@register.simple_tag
def add_random_rubrics_to_context(k=2):
    k = min(len(rubrics), k)
    return {'rubrics': random.sample(list(rubrics), k=k)}

@register.filter
def shuffle(queryset):
    queryset = list(queryset)
    random.shuffle(queryset)
    return queryset

@register.filter
def slice_to_3(queryset, part):
    koef = (len(queryset) + 2) // 3
    return queryset[(part-1)*koef:part*koef]


