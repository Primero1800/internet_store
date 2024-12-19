from decimal import Decimal

import django_filters
from django.db import models
from django.db.models import QuerySet, Count, F
from django_filters.filters import OrderingFilter

from orders.inner_functions import _separator_normalize
from orders.models import Address, Order, Person
from posts.models import Post
from store.models import Brand, Product, Rubric


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


class OrderOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('total_price', 'total_price'), ('-total_price', 'total_price (descending)'),
            ('id', 'id'), ('-id', 'id (descending)'),
            ('time_placed', 'time_placed'), ('-time_placed', 'time_placed (descending)'),
            ('time_delivered', 'time_delivered'), ('-time_delivered', 'time_delivered (descending)'),
        ]


class OrderFilter(django_filters.FilterSet):
    o = OrderOrderingFilter()
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


class PersonOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('user', 'user'), ('-user', 'user (descending)'),
        ]


class PersonFilter(django_filters.FilterSet):
    o = PersonOrderingFilter()
    class Meta:
        model = Person
        fields = ('user', )


class PostOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('user', 'user'), ('-user', 'user (descending)'),
            ('product', 'product'), ('-product', 'product (descending)'),
        ]


class PostFilter(django_filters.FilterSet):
    o = PostOrderingFilter()
    class Meta:
        model = Post
        fields = {
            'id': ['exact', ],
            'user': ['exact'],
            'product': ['exact']
        }


class ProductOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('title', 'title'), ('-title', 'title (descending)'),
            ('brand', 'brand'), ('-brand', 'brand (descending)'),
            ('calculated_price', 'price'), ('-calculated_price', 'price (descending)'),
            ('discont', 'discont'), ('-discont', 'discont (descending)'),
            ('quantity', 'quantity'), ('-quantity', 'quantity (descending)'),
            ('rating', 'rating'), ('-rating', 'rating (descending)'),
            ('rubrics__count', 'rubrics_count'), ('-rubrics__count', 'rubrics_count (descending)'),
        ]

    def filter(self, query_set, values):
        if not values:
            return super().filter(query_set, values)
        for value in values:
            if value in ('rubrics__count', '-rubrics__count'):
                return query_set.annotate(Count('rubrics')).order_by(value)
            elif value in ('calculated_price', '-calculated_price'):
                return query_set.annotate(calculated_price=(100-F('discont'))*F('start_price')/100).order_by(value)
            else:
                return query_set.order_by(value)
        return super().filter(query_set, values)


class ProductFilter(django_filters.FilterSet):
    o = ProductOrderingFilter()

    class Meta:
        model = Product
        fields = {
            'title': ['contains', ],
            'brand': ['exact', ],
            'rubrics': ['exact', ],
            'discont': ['gte', ],
            'quantity': ['lte',],
        }


class RubricOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
             ('id', 'id'), ('-id', 'id (descending)'),
             ('title', 'title'), ('-title', 'title (descending)'),
             ('products__count', 'products_count'), ('-products__count', 'products_count (descending)'),
        ]

    def filter(self, query_set, values):
        if not values:
            return super().filter(query_set, values)
        for value in values:
            if value in ('products__count', '-products__count'):
                return query_set.annotate(Count('products')).order_by(value)
            else:
                return query_set.order_by(value)
        return super().filter(query_set, values)


class RubricFilter(django_filters.FilterSet):
    o = RubricOrderingFilter()

    class Meta:
        model = Rubric
        fields = {
             'products': ['exact', ],
        }