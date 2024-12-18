import django_filters
from django_filters import filters

from orders.models import Address
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