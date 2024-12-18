import django_filters
from django.db import models
from django_filters import filters

from orders.models import Address, Order
from store.models import Brand


class AddressFilter(django_filters.FilterSet):
    city = filters.CharFilter()
    class Meta:
        model = Address
        fields = {
            'city': ['exact', ],
            'id': ['exact', 'gte', 'lte'],
            'user': ['exact',],
            'phonenumber': ['exact' , 'contains']
        }


class BrandFilter(django_filters.FilterSet):
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