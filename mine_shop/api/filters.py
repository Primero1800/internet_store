import django_filters
from django.db import models
from django.db.models import QuerySet, Count
from django_filters.filters import OrderingFilter

from orders.models import Address, Order
from store.models import Brand
class AddressOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('user', 'user'), ('-user', 'user (descending)'),
            ('phonenumber', 'phonenumber'), ('-phonenumber', 'phonenumber (descending)'),
        ]


class AddressFilter(django_filters.FilterSet):
    o = AddressOrderingFilter()
    class Meta:
        model = Address
        fields = {
            'city': ['exact', ],
            'id': ['exact', 'gte', 'lte'],
            'user': ['exact',],
            'phonenumber': ['exact' , 'contains']
        }


class BrandOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('items__count', 'products_count'), ('-items__count', 'products_count (descending)'),
            ('id', 'id'), ('-id', 'id (descending)'),
            ('title', 'title'), ('-title', 'title (descending)'),
        ]

    def filter(self, query_set, values):
        if not values:
            return super().filter(query_set, values)

        for value in values:
            if value in ('items__count', '-items__count'):
                return query_set.annotate(Count('items')).order_by(value)
            else:
                return query_set.order_by(value)
        return super().filter(query_set, values)


class BrandFilter(django_filters.FilterSet):
    o = BrandOrderingFilter()

    class Meta:
        model = Brand
        fields = {
            'id': ['exact'],
            'title': ['exact', 'contains'],
            'items': ['exact'],
        }


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'phonenumber': ['contains',],
            'total_price': ['gte', 'lte',],
            'payment_conditions': ['exact'],
            'status': ['exact'],
            'time_placed': ['range'],
            'time_delivered': ['range'],
        }

    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        if isinstance(f, models.DateTimeField) and lookup_type == 'range':
            return django_filters.DateFromToRangeFilter, {}
        return super().filter_for_lookup(f, lookup_type)