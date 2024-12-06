import json
from decimal import Decimal

from rest_framework import serializers

from orders.inner_functions import _separator_normalize
from orders.models import Order
from posts.models import Post
from store.info_classes import Vote
from store.models import Product
from users.models import User


class ProductFreeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'price', 'start_price', 'discont', 'rating', 'available')

    brand = serializers.SerializerMethodField('get_brand')
    def get_brand(self, instance):
        return f"{instance.brand.title} (ID={instance.brand.id})"

    start_price = serializers.SerializerMethodField('get_start_price')
    def get_start_price(self, instance):
        return Decimal(_separator_normalize(instance.start_price))

    price = serializers.SerializerMethodField('get_price')
    def get_price(self, instance):
        return instance.price

    discont = serializers.SerializerMethodField('get_discont')
    def get_discont(self, instance):
        return instance.get_discont_display()

    available = serializers.SerializerMethodField('get_available')
    def get_available(self, instance):
        return instance.get_available_display()


class ProductFullSerializer(ProductFreeFullSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'price', 'start_price', 'discont', 'rating', 'quantity', 'available', 'sale_information', 'feedback_information')

    feedback_information = serializers.SerializerMethodField('get_feedback')
    def get_feedback(self, instance):
        votes = instance.votes.all()
        votes_context = {}
        for vote in votes:
            votes_context.setdefault(vote.stars, [])
            votes_context[vote.stars] .append({
                'name': vote.name,
                'user': str(vote.user),
                'grade': f"*{vote.stars}",
                'review': vote.review
            })
        posts = instance.posts.all()
        posts_context = [{'name': post.name, 'user': post.user.email, 'review': post.review} for post in posts]
        return {
            f"votes < {len(votes)} >": dict(sorted(votes_context.items(), reverse=True)),
            f"posts < {len(posts)} >": posts_context
        }

    sale_information = serializers.SerializerMethodField('get_sale_information')
    def get_sale_information(self, instance):
        try:
            instance.sale_information
            return {
                'sold_count': instance.sale_information.sold_count,
                'viewed_count': instance.sale_information.viewed_count,
                'rating': instance.sale_information.rating / instance.sale_information.voted_count if instance.sale_information.voted_count else instance.sale_information.rating
            }
        except:
            return None



class ProductSerializer(ProductFullSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'available', 'quantity', 'sold')

    sold = serializers.SerializerMethodField('get_sold')
    def get_sold(self, instance):
        try:
            return instance.sale_information.sold_count
        except:
            return 0

class ProductDetailSerializer(ProductFullSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'brand', 'description', 'additional_information', 'images', 'price', 'start_price', 'discont', 'rating', 'quantity', 'available',
                  'sale_information', 'feedback_information', 'orders')

    additional_information = serializers.SerializerMethodField('get_additional_information')
    def get_additional_information(self, instance):
        try:
            instance.additional_information
            return {
                'weight': instance.additional_information.weight,
                'dimensions': instance.additional_information.dimensions,
                'size' : instance.additional_information.size,
            }
        except:
            return None

    images = serializers.SerializerMethodField('get_images')
    def get_images(self, instance):
        return [image.image.url for image in instance.images.all()]

    description = serializers.SerializerMethodField('get_description')
    def get_description(self, instance):
        return [word.strip().strip('\t') for word in instance.description.split('\r\n')]

    orders = serializers.SerializerMethodField('get_orders')
    def get_orders(self, instance):
        result = []
        for order in Order.objects.all():
            if order.status != 2:
                order_content = json.loads(order.order_content)
                for item in order_content:
                    if item['id'] == instance.pk:
                        person = json.loads(order.person_content)
                        address = json.loads(order.address_content)
                        result.append({
                            'id': order.id,
                            'time_placed': order.time_placed,
                            'status': order.get_status_display(),
                            'total_price': order.total_price,
                            'time_delivered': order.time_delivered,
                            'person': person,
                            'address': address,
                            'payment_conditions': order.get_payment_conditions_display(),
                            'move_to': order.get_move_to_display(),
                            'content': item
                        })
        return result


class ProductDetailFreeSerializer(ProductDetailSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'brand', 'description', 'additional_information', 'images', 'price', 'start_price', 'discont', 'rating', 'available', 'feedback_information')

    feedback_information = serializers.SerializerMethodField('get_feedback')
    def get_feedback(self, instance):
        fbi = super().get_feedback(instance)
        votes, posts = tuple(fbi.items())
        votes = list(votes[1].values())
        if votes:
            for vote in votes:
                if 'user' in vote[0]: del vote[0]['user']
        posts = list(posts[1])
        if posts:
            for post in posts:
                if 'user' in post: del post['user']
        return fbi


class OrderFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'time_placed', 'status', 'total_price', 'time_delivered', 'person', 'address', 'payment_conditions', 'move_to', 'content')

    status = serializers.SerializerMethodField('get_status')
    def get_status(self, instance):
        return instance.get_status_display()


    total_price = serializers.SerializerMethodField('get_total_price')
    def get_total_price(self, instance):
        return Decimal(_separator_normalize(instance.total_price))

    person = serializers.SerializerMethodField('get_person')
    def get_person(self, instance):
        return json.loads(instance.person_content)

    address = serializers.SerializerMethodField('get_address')
    def get_address(self, instance):
        return json.loads(instance.address_content)

    move_to = serializers.SerializerMethodField('get_move_to')
    def get_move_to(self, instance):
        return instance.get_move_to_display()

    payment_conditions = serializers.SerializerMethodField('get_payment_conditions')
    def get_payment_conditions(self, instance):
        return instance.get_payment_conditions_display()

    content = serializers.SerializerMethodField('get_content')
    def get_content(self, instance):
        return json.loads(instance.order_content)


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser', 'votes_count', 'posts_count', 'total_spended', 'orders_count', 'orders')

    votes_count = serializers.SerializerMethodField('get_votes_count')
    def get_votes_count(self, instance):
        return len(instance.votes.all())

    posts_count = serializers.SerializerMethodField('get_posts_count')
    def get_posts_count(self, instance):
        return len(instance.posts.all())

    orders_count = serializers.SerializerMethodField('get_orders_count')
    def get_orders_count(self, instance):
        return len(instance.order_set.filter(status__in=(0, 1)))

    total_spended = serializers.SerializerMethodField('get_total_spended')
    def get_total_spended(self, instance):
        return sum(order.total_price for order in instance.order_set.filter(status=1))

    orders = serializers.SerializerMethodField('get_orders')
    def get_orders(self, instance):
        orders = instance.order_set.all()
        serializer = OrderFullSerializer(orders, many=True)
        return serializer.data

class UserSerializer(UserFullSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser', 'orders_count', 'total_spended')