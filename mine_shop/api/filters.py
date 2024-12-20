import django_filters
from django.db import models
from django.db.models import Count, F, Case, When
from django_filters import filters
from django_filters.filters import OrderingFilter

from orders.models import Address, Order, Person
from posts.models import Post
from store.info_classes import Sale_information
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


class SaleInformationOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('product_id', 'product_id'), ('-product_id', 'product_id (descending)'),
            ('product__title', 'product_title'), ('-product__title', 'product_title (descending)'),
            ('sold_count', 'sold_count'), ('-sold_count', 'sold_count (descending)'),
            ('viewed_count', 'viewed_count'), ('-viewed_count', 'viewed_count (descending)'),
            ('calculated_rating', 'rating'), ('-calculated_rating', 'rating (descending)'),
        ]

    def filter(self, query_set, values):
        if not values:
            return super().filter(query_set, values)
        for value in values:
            if value in ('calculated_rating', '-calculated_rating'):
                return query_set.annotate(
                     calculated_rating=Case(
                         When(voted_count__gt=0, then=100*F('rating')/F('voted_count')),
                                         When(voted_count=0, then=100*F('rating')),
                     )
                 ).order_by(value)
            else:
                return query_set.order_by(value)
        return super().filter(query_set, values)


class SaleInformationFilter(django_filters.FilterSet):
    class Meta:
        model = Sale_information
        fields = {
            'sold_count': ['gte', 'lte',],
            'viewed_count': ['gte', 'lte', ],
        }

    class RatingGTEFilter(filters.NumberFilter):
        def filter(self, qs, value):
            if not value:
                return qs
            return qs.annotate(
                calculated_rating=Case(
                    When(voted_count__gt=0, then=100 * F('rating') / F('voted_count')),
                    When(voted_count=0, then=100 * F('rating')),
                )
            ).filter(calculated_rating__gte=value * 100)

    class RatingLTEFilter(filters.NumberFilter):

        def filter(self, qs, value):
            if not value:
                return qs
            return qs.annotate(
                calculated_rating=Case(
                    When(voted_count__gt=0, then=100 * F('rating') / F('voted_count')),
                    When(voted_count=0, then=100 * F('rating')),
                )
            ).filter(calculated_rating__lte=value * 100)

    calculated_rating__gte = RatingGTEFilter(field_name='rating', lookup_expr='__gte')
    calculated_rating__lte = RatingLTEFilter(field_name='rating', lookup_expr='__lte')

    o = SaleInformationOrderingFilter()

