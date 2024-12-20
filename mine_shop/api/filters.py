from django_filters import FilterSet
from django.db.models import Count, F, Case, When, DateTimeField
from django_filters.filters import OrderingFilter, NumberFilter, DateFromToRangeFilter
from orders.models import Address, Order, Person
from posts.models import Post
from store.info_classes import Sale_information, Vote
from store.models import Brand, Product, Rubric
from users.models import User


class AddressOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('user', 'user'), ('-user', 'user (descending)'),
            ('phonenumber', 'phonenumber'), ('-phonenumber', 'phonenumber (descending)'),
        ]


class AddressFilter(FilterSet):
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


class BrandFilter(FilterSet):
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


class OrderFilter(FilterSet):
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
        if isinstance(f, DateTimeField) and lookup_type == 'range':
            return DateFromToRangeFilter, {}
        return super().filter_for_lookup(f, lookup_type)


class PersonOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('user', 'user'), ('-user', 'user (descending)'),
        ]


class PersonFilter(FilterSet):
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


class PostFilter(FilterSet):
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


class ProductFilter(FilterSet):
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


class RubricFilter(FilterSet):
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


class SaleInformationFilter(FilterSet):
    class Meta:
        model = Sale_information
        fields = {
            'sold_count': ['gte', 'lte',],
            'viewed_count': ['gte', 'lte', ],
        }

    class RatingFilter(NumberFilter):
        def filter(self, qs, value):
            if not value:
                return qs
            result_qs = qs.annotate(
                calculated_rating=Case(
                    When(voted_count__gt=0, then=100 * F('rating') / F('voted_count')),
                    When(voted_count=0, then=100 * F('rating')),
                )
            )
            if self.lookup_expr == '__gte':
                return result_qs.filter(calculated_rating__gte=value * 100)
            else:
                return result_qs.filter(calculated_rating__lte=value * 100)

    calculated_rating__gte = RatingFilter(field_name='rating', lookup_expr='__gte')
    calculated_rating__lte = RatingFilter(field_name='rating', lookup_expr='__lte')

    o = SaleInformationOrderingFilter()


class UserOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
        ]


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            "email": ['contains'],
            "is_active": ['exact'],
            "is_staff": ['exact'],
            "is_superuser": ['exact'],
        }

    o = UserOrderingFilter()


class VoteOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('id', 'id'), ('-id', 'id (descending)'),
            ('stars', 'stars'), ('-stars', 'stars (descending)'),
            ('user__id', 'user'), ('-user__id', 'user (descending)'),
            ('product__id', 'product'), ('-product__id', 'product (descending)'),
        ]


class VoteFilter(FilterSet):
    class Meta:
        model = Vote
        fields = {
            'user': ['exact',],
            'product': ['exact', ],
            'stars': ['gte', 'lte'],
            'time_published': ['range'],
        }

    o = VoteOrderingFilter()

    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        if isinstance(f, DateTimeField) and lookup_type == 'range':
            return DateFromToRangeFilter, {}
        return super().filter_for_lookup(f, lookup_type)
