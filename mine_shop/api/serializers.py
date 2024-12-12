from rest_framework import serializers

from cart.models import Cart, CartItem
from orders.models import Order, Person, Address
from posts.models import Post
from store.info_classes import Vote
from store.models import Product, Brand, Rubric
from users.models import User, WishlistItem, ComparisonItem, RecentlyViewedItem, UserTools


class UserTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class ProductTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title')



class UserToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTools
        fields = ('user',)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'user', 'name', 'surname', 'company_name')

    user = serializers.SerializerMethodField('get_short_user')
    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data

class PersonInSerializer(PersonSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'surname', 'company_name')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'address', 'city',  'phonenumber')

    user = serializers.SerializerMethodField('get_short_user')
    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data


class AddressInSerializer(AddressSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address', 'city',  'phonenumber')


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

class RubricInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'title')

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'title', 'slug', 'description', 'image', 'products')

    products = serializers.SerializerMethodField('get_short_products')
    def get_short_products(self, instance):
        queryset = instance.products.all()
        serializer = ProductTitlesSerializer(queryset, many=True)
        return serializer.data

class BrandInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title', 'description', 'image', 'products')

    products = serializers.SerializerMethodField('get_short_products')
    def get_short_products(self, instance):
        queryset = instance.items.all()
        serializer = ProductTitlesSerializer(queryset, many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_active', 'is_staff', 'is_superuser')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'phonenumber', 'order_content', 'person_content', 'address_content', 'total_price', 'move_to', 'payment_conditions', 'status', 'time_placed', 'time_delivered')

    user = serializers.SerializerMethodField('get_short_user')
    def get_short_user(self, instance):
        queryset = instance.user
        serializer = UserTitlesSerializer(queryset)
        return serializer.data

class OrderInSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'phonenumber', 'order_content', 'person_content', 'address_content', 'total_price', 'move_to',
            'payment_conditions', 'status', 'time_placed', 'time_delivered',
        )

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'price', 'total_price')

    product = serializers.SerializerMethodField('get_short_product')
    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

class CartSerializer(serializers.ModelSerializer):
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
        serializer = CartItemSerializer(queryset, many=True)
        return serializer.data


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ('id', 'product')

    product = serializers.SerializerMethodField('get_short_product')
    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

class ComparisonItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonItem
        fields = ('id', 'product')

    product = serializers.SerializerMethodField('get_short_product')
    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data

class RecentlyViewedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentlyViewedItem
        fields = ('id', 'product')

    product = serializers.SerializerMethodField('get_short_product')
    def get_short_product(self, instance):
        queryset = instance.product
        serializer = ProductTitlesSerializer(queryset)
        return serializer.data


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
        queryset = instance.usertools
        serializer = UserToolsSerializer(queryset)
        return serializer.data

    person = serializers.SerializerMethodField('get_person')
    def get_person(self, instance):
        queryset = instance.person
        serializer = PersonInSerializer(queryset)
        return serializer.data

    address = serializers.SerializerMethodField('get_address')
    def get_address(self, instance):
        queryset = instance.address
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
        queryset =  instance.order_set.filter(status__in=(0, 1))
        serializer = OrderInSerializer(queryset, many=True)
        return serializer.data

    total_paid = serializers.SerializerMethodField('get_total_paid')
    def get_total_paid(self, instance):
        return sum(order.total_price for order in instance.order_set.filter(status=1))

    cart = serializers.SerializerMethodField('get_cart')
    def get_cart(self, instance):
        queryset = instance.cart
        serializer = CartSerializer(queryset)
        return serializer.data

    wishlist = serializers.SerializerMethodField('get_wishlist')
    def get_wishlist(self, instance):
        queryset = instance.usertools.w_items.all()
        serializer = WishlistItemSerializer(queryset, many=True)
        return serializer.data

    comparison = serializers.SerializerMethodField('get_comparison')
    def get_comparison(self, instance):
        queryset = instance.usertools.c_items.all()
        serializer = ComparisonItemSerializer(queryset, many=True)
        return serializer.data

    recently_viewed = serializers.SerializerMethodField('get_recently_viewed')
    def get_recently_viewed(self, instance):
        queryset = instance.usertools.rv_items.all()
        serializer = RecentlyViewedItemSerializer(queryset, many=True)
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'brand', 'rubrics', 'start_price', 'discont', 'price', 'rating', 'available', 'quantity')

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'slug', 'brand', 'description', 'rubrics', 'start_price', 'discont', 'price', 'rating',
            'available', 'quantity', 'images', 'additional_information', 'sale_information', 'posts', 'votes', 'orders',
            'wishlists', 'comparisons', 'cartitems',
        )

        brand = serializers.SerializerMethodField('get_brand')
        def get_brand(self, instance):
            queryset = instance.brand
            serializer = BrandInSerializer(queryset)
            return serializer.data

        rubrics = serializers.SerializerMethodField('get_rubrics')
        def get_rubrics(self, instance):
            queryset = instance.rubrics.all()
            serializer - RubricInSerializer(queryset, many=True)
            return serializer.data