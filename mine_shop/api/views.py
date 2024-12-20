from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.decorators import permission_classes
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from cart.models import Cart, CartItem
from .filters import AddressFilter, BrandFilter, OrderFilter, PersonFilter, PostFilter, \
    ProductFilter, RubricFilter, SaleInformationFilter, UserFilter, VoteFilter
from orders.models import Person, Address, Order
from posts.models import Post
from store.info_classes import Vote, Sale_information
from store.models import Product, Brand, Rubric
from users.models import User
from .permissions import IsAdminAndOwnerOrReadOnly, IsPosterAdminAndOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    UserSerializer, UserDetailSerializer, PersonSerializerRaw, AddressSerializer, VoteSerializer,
    OrderSerializer, ProductSerializer, BrandSerializer, RubricSerializer, SaleInformationSerializer,
    ProductDetailSerializer, AddressSerializerRaw, CartSerializerRaw, CartItemSerializer,
    PersonSerializer, PostSerializerRaw, ProductSerializerRaw, RubricSerializerRaw
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReadUpdateModelViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    pass


class ReadUpdateDestroyModelViewSet(
    DestroyModelMixin,
    ReadUpdateModelViewSet,
):
    pass


class ReadDestroyModelViewSet(
    DestroyModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    pass


@permission_classes((IsAdminUser, ))
class APIAddressViewSet(ReadUpdateDestroyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    serializer_class_raw = AddressSerializerRaw
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AddressFilter

    def get_serializer_class(self):
        if self.action in ('destroy', 'retrieve', 'update', 'partial_update', ):
             return self.serializer_class_raw
        return self.serializer_class


@permission_classes((IsAdminAndOwnerOrReadOnly,))
class APIBrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = BrandFilter


@permission_classes((IsAdminUser,))
class APICartViewSet(ReadDestroyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializerRaw
    pagination_class = StandardResultsSetPagination


@permission_classes((IsAdminUser,))
class APICartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = StandardResultsSetPagination


@permission_classes((IsAdminUser, ))
class APIOrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrderFilter
    search_fields = ('order_content', )


@permission_classes((IsAdminUser, ))
class APIPersonViewSet(ReadUpdateDestroyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    serializer_class_raw = PersonSerializerRaw
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonFilter

    def get_serializer_class(self):
        if self.action in ('destroy', 'retrieve', 'update', 'partial_update', ):
             return self.serializer_class_raw
        return self.serializer_class


@permission_classes((IsPosterAdminAndOwnerOrReadOnly,))
class APIPostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerRaw
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@permission_classes((IsAdminOrReadOnly,))
class APIProductViewSet(ReadUpdateModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerRaw
    serializer_class_list = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ('title', 'description', )

    def get_serializer_class(self):
        if self.action == 'list':
             return self.serializer_class_list
        return self.serializer_class


@permission_classes((IsAdminUser, ))
class APIProductView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


@permission_classes((IsAdminUser,))
class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    serializer_class_raw = RubricSerializerRaw
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RubricFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get'):
             return self.serializer_class
        return self.serializer_class_raw


@permission_classes((IsAdminUser,))
class APISaleInformationViewSet(ReadOnlyModelViewSet):
    queryset = Sale_information.objects.all()
    serializer_class = SaleInformationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SaleInformationFilter
    search_fields = ('product__title', )


@permission_classes((IsAdminUser, ))
class APIUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = UserFilter


@permission_classes((IsAdminUser, ))
class APIUserView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


@permission_classes((IsAdminOrReadOnly,))
class APIVoteViewSet(ReadOnlyModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = VoteFilter
    search_fields = ('review', 'name')
