from decimal import Decimal

from django.conf import settings
from django.utils.datastructures import MultiValueDict
from django.utils.text import slugify

from rest_framework import serializers

from api.inner_functions import cyr_to_lat
from cart.models import Cart, CartItem
from orders.inner_functions import get_complex_phonenumber, _separator_normalize
from orders.models import Order, Person, Address
from posts.models import Post
from store.info_classes import Vote, Sale_information
from store.models import Product, Brand, Rubric, Image, Additional_information
from users.models import User, WishlistItem, ComparisonItem, RecentlyViewedItem, UserTools

from phonenumber_field.serializerfields import PhoneNumberField


class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional_information
        fields = ('id', 'weight', 'dimensions', 'size', 'guarantee')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'address', 'city',  'phonenumber', 'postcode')

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class AddressInSerializer(AddressSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address', 'city',  'phonenumber')


class AddressSerializerRaw(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address', 'city', 'postcode', 'email', 'phonenumber')
        read_only_fields = ('user', 'id', 'email')

    email = serializers.SerializerMethodField('get_email')

    def get_email(self, instance):
        return instance.user.email

    class FormNumberField(serializers.CharField):
        """ Класс для валидации, приведения к общему виду и сериализации телефонного номера и определения региона"""
        def to_internal_value(self, data):
            if not data or isinstance(data, bool) or not isinstance(data, (str, int, float,)):
                self.fail('invalid')
            value = str(data).split(settings.PHONE_NUMBER_DATABASE_SEPARATOR.strip())
            _region = ''.join(symbol.upper() for symbol in value[0] if symbol.isalpha())[:2]
            _number = ''.join([digit for digit in value[-1] if digit.isdigit()])
            if not _region or not _number:
                self.fail('invalid')
            if _region not in settings.PHONE_NUMBER_ALOWED_REGIONS:
                self.fail('not allowed')
            _region_prefix = settings.PHONE_NUMBER_ALOWED_REGIONS[_region]

            class PhoneNumberSerializer(serializers.Serializer):
                """Класс для проверки телефонного номера, принадлежности его к
                установленному региону и извлечению регионального номера"""
                number = PhoneNumberField(region=_region)

            _serializer = PhoneNumberSerializer(data={"number": _number})
            if _serializer.is_valid():
                _data = _serializer.validated_data
                return get_complex_phonenumber(country_code=_region, phone_number=str(_data['number'].national_number))
            else:
                self.fail('not number')

    phonenumber = FormNumberField(error_messages={
        'not allowed': "Invalid or not allowed region",
        'not number': "Not valid phone number",
    })


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title', 'description', 'image', 'products_count', 'products', )

    products_count = serializers.SerializerMethodField('get_products_count')
    products = serializers.SerializerMethodField('get_short_products')

    def get_short_products(self, instance):
        queryset = instance.items.all()
        serializer = ProductTitlesSerializer(queryset, many=True)
        return serializer.data

    def get_products_count(self, instance):
        return instance.get_products_count()


class BrandInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title')


class CartSerializerRaw(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'total_price', 'cart_items')

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data

    cart_items = serializers.SerializerMethodField('get_cart_items')

    def get_cart_items(self, instance):
        queryset = instance.cart_items.all()
        serializer = CartItemInUserSerializer(queryset, many=True)
        return serializer.data


class CartSerializerInUser(CartSerializerRaw):
    class Meta:
        model = Cart
        fields = ('id', 'total_price', 'cart_items')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('price',)

    def _get_product(self):
        try:
            self.product
        except:
            self.product = None
        if not self.product:
            self.product = Product.objects.get(id=int(self.context['request'].POST['product']))

    class PriceField(serializers.CharField):
        def to_internal_value(self, data):
            if data:
                data = str(data)
            if 'product' in self.context['request'].POST:
                self.parent._get_product()
                data = str(self.parent.product.price)
            return data

    class QuantityField(serializers.IntegerField):
        def to_internal_value(self, data):
            if not data:
                self.fail('invalid')
            try:
                data = int(data.strip())
            except:
                self.fail('invalid')
            if data < 1:
                self.fail('negative')
            if 'product' in self.context['request'].POST:
                self.parent._get_product()
                data = min(self.parent.product.quantity, data)
                if data == 0:
                    self.fail('not in stock')
            return data

    price = PriceField(initial='0', allow_blank=True, allow_null=True)
    quantity = QuantityField(initial=1, error_messages={
        'negative': "A positive integer is required",
        'not in stock': "Chosen product not in stock, try another one"
    },
    )


class CartItemInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'price', 'total_price')

    product = serializers.SerializerMethodField('get_short_product')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data


class CartItemInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('user', 'quantity', 'price', 'total_price')

    user = serializers.SerializerMethodField('get_cart_user')

    def get_cart_user(self, instance):
        queryset = instance.cart.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class ComparisonItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonItem
        fields = ('id', 'product', 'user')

    product = serializers.SerializerMethodField('get_short_product')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.recently_viewed.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class ComparisonItemInUserSerializer(ComparisonItemSerializer):
    class Meta:
        model = ComparisonItem
        fields = ('id', 'product')


class ComparisonItemInProductSerializer(ComparisonItemSerializer):
    class Meta:
        model = ComparisonItem
        fields = ('id', 'user')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'user', 'phonenumber', 'order_content', 'person_content', 'address_content',
            'total_price', 'move_to', 'payment_conditions', 'status', 'time_placed', 'time_delivered'
        )

    user = serializers.SerializerMethodField('get_short_user')
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data

    def get_total_price(self, instance):
        return Decimal(_separator_normalize(instance.total_price))


class OrderInSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'phonenumber', 'order_content', 'person_content', 'address_content', 'total_price', 'move_to',
            'payment_conditions', 'status', 'time_placed', 'time_delivered',
        )


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'user', 'name', 'surname', 'company_name')

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class PersonSerializerRaw(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'user', 'name', 'surname', 'company_name')
        read_only_fields = ('user', )

    user = serializers.SlugRelatedField(slug_field='email', read_only=True)


class PersonInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'surname', 'company_name')


class PostSerializerRaw(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'name', 'product', 'review', 'time_published')
        read_only_fields = ('user', )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'name', 'product', 'review', 'time_published')

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data

    product = serializers.SerializerMethodField('get_short_product')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data


class PostInUserSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ('id', 'name', 'product', 'review', 'time_published')


class PostInProductSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'name', 'review', 'time_published')


class ProductSerializerRaw(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'slug', 'brand', 'rubrics', 'start_price', 'discont',
            'price', 'rating', 'calculated_rating', 'available', 'quantity'
        )
        read_only_fields = ('rating', )

    calculated_rating = serializers.SerializerMethodField('get_calculated_rating')

    def get_calculated_rating(self, instance):
        try:
            result = instance.sale_information.rating / instance.sale_information.voted_count if instance.sale_information.voted_count else instance.sale_information.rating
            return Decimal(result)
        except:
            return None


class ProductSerializer(ProductSerializerRaw):
    rubrics = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)
    brand = serializers.SlugRelatedField(slug_field='title', read_only=True)


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'slug', 'brand', 'description', 'rubrics', 'start_price', 'discont', 'price', 'rating',
            'available', 'quantity', 'images', 'additional_information', 'sale_information', 'posts', 'votes',
            'wishlists', 'comparisons', 'recently_viewed', 'cartitems',
        )

    brand = serializers.SerializerMethodField('get_brand')

    def get_brand(self, instance):
        queryset = instance.brand
        serializer = BrandInSerializer(queryset)
        return serializer.data

    rubrics = serializers.SerializerMethodField('get_rubrics')

    def get_rubrics(self, instance):
        queryset = instance.rubrics.all()
        serializer = RubricInSerializer(queryset, many=True)
        return serializer.data

    images = serializers.SerializerMethodField('get_images')

    def get_images(self, instance):
        queryset = instance.images.all()
        serializer = ImageSerializer(queryset, many=True)
        return serializer.data

    additional_information = serializers.SerializerMethodField('get_additional_information')

    def get_additional_information(self, instance):
        queryset = instance.additional_information
        serializer = AdditionalInformationSerializer(queryset)
        return serializer.data

    sale_information = serializers.SerializerMethodField('get_sale_information')

    def get_sale_information(self, instance):
        queryset = instance.sale_information
        serializer = SaleInformationInSerializer(queryset)
        return serializer.data

    posts = serializers.SerializerMethodField('get_posts')

    def get_posts(self, instance):
        queryset = instance.posts.all()
        serializer = PostInProductSerializer(queryset, many=True)
        return serializer.data

    votes = serializers.SerializerMethodField('get_votes')

    def get_votes(self, instance):
        queryset = instance.votes.all()
        serializer = VoteInProductSerializer(queryset, many=True)
        return serializer.data

    wishlists = serializers.SerializerMethodField('get_wishlists')

    def get_wishlists(self, instance):
        queryset = instance.wishlistitem_set.all()
        serializer = WishlistItemInProductSerializer(queryset, many=True)
        return serializer.data

    comparisons = serializers.SerializerMethodField('get_comparisons')

    def get_comparisons(self, instance):
        queryset = instance.comparisonitem_set.all()
        serializer = ComparisonItemInProductSerializer(queryset, many=True)
        return serializer.data

    cartitems = serializers.SerializerMethodField('get_cartitems')

    def get_cartitems(self, instance):
        queryset = instance.cartitem_set.all()
        serializer = CartItemInProductSerializer(queryset, many=True)
        return serializer.data

    recently_viewed = serializers.SerializerMethodField('get_recently_viewed')

    def get_recently_viewed(self, instance):
        queryset = instance.recentlyvieweditem_set.all()
        serializer = RecentlyViewedItemInProductSerializer(queryset, many=True)
        return serializer.data


class ProductTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title')


class RecentlyViewedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentlyViewedItem
        fields = ('id', 'product', 'user')

    product = serializers.SerializerMethodField('get_short_product')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.recently_viewed.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class RecentlyViewedItemInUserSerializer(RecentlyViewedItemSerializer):
    class Meta:
        model = RecentlyViewedItem
        fields = ('id', 'product', )


class RecentlyViewedItemInProductSerializer(RecentlyViewedItemSerializer):
    class Meta:
        model = RecentlyViewedItem
        fields = ('id', 'user')


class RubricInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'title')


class RubricSerializerRaw(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'title', 'slug', 'description', 'image', 'products')

    def is_valid(self, raise_exception=False):
        initial_data = MultiValueDict(self.initial_data)
        initial_data['slug'] = cyr_to_lat(slugify(self.context['request'].POST['title'], allow_unicode=True))
        self.initial_data = initial_data
        return super().is_valid(raise_exception=raise_exception)


class RubricSerializer(RubricSerializerRaw):
    class Meta:
        model = Rubric
        fields = ('id', 'title', 'slug', 'description', 'image', 'products')

    products = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)


class SaleInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale_information
        fields = ('id', 'product', 'calculated_rating', 'sold_count', 'viewed_count', 'voted_count')

    product = serializers.SerializerMethodField('get_short_product')
    calculated_rating = serializers.SerializerMethodField('get_calculated_rating')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

    def get_calculated_rating(self, instance):
        result = instance.rating if not instance.voted_count else instance.rating / instance.voted_count
        return Decimal(result)


class SaleInformationInSerializer(SaleInformationSerializer):
    class Meta:
        model = Sale_information
        fields = ('id', 'calculated_rating', 'sold_count', 'viewed_count', 'voted_count')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_active', 'is_staff', 'is_superuser')
        write_only_fields = ('password',)

    password = serializers.CharField(
        min_length=8, required=True, write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'is_active', 'is_staff', 'is_superuser', 'person', 'address', 'posts_count', 'posts',
            'votes_count', 'votes', 'orders_count', 'total_paid', 'orders', 'cart', 'usertools',
            'wishlist', 'comparison', 'recently_viewed',
        )

    usertools = serializers.SerializerMethodField('get_usertools')

    def get_usertools(self, instance):
        try:
            queryset = instance.usertools
        except:
            return None
        serializer = UserToolsSerializer(queryset)
        return serializer.data

    person = serializers.SerializerMethodField('get_person')

    def get_person(self, instance):
        try:
            queryset = instance.person
        except:
            return None
        serializer = PersonInSerializer(queryset)
        return serializer.data

    address = serializers.SerializerMethodField('get_address')

    def get_address(self, instance):
        try:
            queryset = instance.address
        except:
            return None
        serializer = AddressInSerializer(queryset)
        return serializer.data

    votes_count = serializers.SerializerMethodField('get_votes_count')

    def get_votes_count(self, instance):
        return len(instance.votes.all())

    votes = serializers.SerializerMethodField('get_votes')

    def get_votes(self, instance):
        queryset = instance.votes
        serializer = VoteInUserSerializer(queryset, many=True)
        return serializer.data

    posts_count = serializers.SerializerMethodField('get_posts_count')

    def get_posts_count(self, instance):
        return len(instance.posts.all())

    posts = serializers.SerializerMethodField('get_posts')

    def get_posts(self, instance):
        queryset = instance.posts.all()
        serializer = PostInUserSerializer(queryset, many=True)
        return serializer.data

    orders_count = serializers.SerializerMethodField('get_orders_count')

    def get_orders_count(self, instance):
        return len(instance.order_set.filter(status__in=(0, 1)))

    orders = serializers.SerializerMethodField('get_orders')

    def get_orders(self, instance):
        queryset = instance.order_set.filter(status__in=(0, 1))
        serializer = OrderInSerializer(queryset, many=True)
        return serializer.data

    total_paid = serializers.SerializerMethodField('get_total_paid')

    def get_total_paid(self, instance):
        return sum(order.total_price for order in instance.order_set.filter(status=1))

    cart = serializers.SerializerMethodField('get_cart')

    def get_cart(self, instance):
        try:
            queryset = instance.cart
        except:
            return None
        serializer = CartSerializerInUser(queryset)
        return serializer.data

    wishlist = serializers.SerializerMethodField('get_wishlist')

    def get_wishlist(self, instance):
        try:
            queryset = instance.usertools.w_items.all()
        except:
            return None
        serializer = WishlistItemInUserSerializer(queryset, many=True)
        return serializer.data

    comparison = serializers.SerializerMethodField('get_comparison')

    def get_comparison(self, instance):
        try:
            queryset = instance.usertools.c_items.all()
        except:
            return None
        serializer = ComparisonItemInUserSerializer(queryset, many=True)
        return serializer.data

    recently_viewed = serializers.SerializerMethodField('get_recently_viewed')

    def get_recently_viewed(self, instance):
        try:
            queryset = instance.usertools.rv_items.all()
        except:
            return None
        serializer = RecentlyViewedItemInUserSerializer(queryset, many=True)
        return serializer.data


class UserTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class UserToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTools
        fields = ('user',)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'user', 'name', 'product', 'stars', 'review', 'time_published')

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data

    product = serializers.SerializerMethodField('get_short_product')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data


class VoteInUserSerializer(VoteSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'name', 'product', 'stars', 'review', 'time_published')


class VoteInProductSerializer(VoteSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'user', 'name', 'stars', 'review', 'time_published')


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ('id', 'user', 'product')

    product = serializers.SerializerMethodField('get_short_product')

    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

    user = serializers.SerializerMethodField('get_short_user')

    def get_short_user(self, instance):
        queryset = instance.recently_viewed.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class WishlistItemInUserSerializer(WishlistItemSerializer):
    class Meta:
        model = WishlistItem
        fields = ('id', 'product')


class WishlistItemInProductSerializer(WishlistItemSerializer):
    class Meta:
        model = WishlistItem
        fields = ('id', 'user')
