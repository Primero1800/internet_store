from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from orders.models import Order
from store.models import Product
from users.models import User
from .inner_functions import filters
from .serializers import ProductFullSerializer, ProductSerializer, ProductDetailSerializer, ProductFreeFullSerializer, \
    ProductDetailFreeSerializer, OrderFullSerializer, UserFullSerializer, UserSerializer


@api_view(['GET'])
def products_short_free(request, count=None, sort_by=None):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductFreeFullSerializer(products, many=True)
        data = filters(queryset=serializer.data, count=count, sort_by=sort_by, x_filters_mapping={
            'id': None, 'title': 'title', 'available': 'available', 'price': 'price', 'start_price': 'start_price',
            'discont': 'discont', 'rating': 'rating', 'brand': 'brand',
        }, other='id')
        return Response(data)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def products_short(request, count=None, sort_by=None):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        data = filters(queryset=serializer.data, count=count, sort_by=sort_by, x_filters_mapping={
            'id': None, 'sold': 'sold', 'title': 'title', 'available': 'available',
        }, other='quantity')

        return Response(data)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def products_full(request, count=None, sort_by=None):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductFullSerializer(products, many=True)

        data = filters(queryset=serializer.data, count=count, sort_by=sort_by, x_filters_mapping={
            'id': None,
            'title': 'title',
            'brand': 'brand',
            'price': 'price',
            'discont': 'discont',
            'rating': 'rating',
            'available': 'available',
            'quantity': 'quantity',
            'start_price': 'start_price',
        },
                       dict_mapping={
                           'sale_information': 'sold_count',
                           'feedback_information': None,
                       },
                       other=None)

        return Response(data)


@permission_classes((IsAdminUser,))
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductDetailFreeView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailFreeSerializer


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def orders(request, count=None, sort_by=None):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderFullSerializer(orders, many=True)

        data = filters(queryset=serializer.data, count=count, sort_by=sort_by, x_filters_mapping={
            'id': None, 'status': 'status', 'total_price': 'total_price', 'time_placed': 'time_placed',
            'content': 'total_price',
        },
                       dict_mapping={
                           'person': 'name',
                           'address': 'phonenumber',
                       },
                       other='id')

        return Response(data)


@permission_classes((IsAdminUser,))
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFullSerializer


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def users(request, count=None, sort_by=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        data = filters(queryset=serializer.data, count=count, sort_by=sort_by, x_filters_mapping={
            'id': None, 'email': 'email', 'username': 'username', 'is_active': 'is_active',
            'is_superuser': 'is_superuser', 'is_staff': 'is_staff', 'orders_count': 'orders_count',
            'total_spended': 'total_spended',
        }, other='id')

        return Response(data)


from django.shortcuts import render

# Create your views here.
