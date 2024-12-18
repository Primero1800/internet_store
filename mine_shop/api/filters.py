import django_filters
from django_filters import filters

from orders.models import Address


class AddressFilter(django_filters.FilterSet):
    city = filters.CharFilter()
    class Meta:
        model = Address
        fields = {
            'city': ['exact', ],
            'id': ['exact',],
            'user': ['exact',],
            'phonenumber': ['exact' , 'contains']
        }