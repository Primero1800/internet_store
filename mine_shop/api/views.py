from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
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
    PersonSerializer, PostSerializerRaw, ProductSerializerRaw, RubricSerializerRaw, ErrorSerializer
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
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список связанных адресов (доступно только для администрации сайта)"),
            responses={
                        status.HTTP_200_OK: AddressSerializer,
                        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
                        status.HTTP_401_UNAUTHORIZED: ErrorSerializer,
                        status.HTTP_403_FORBIDDEN: ErrorSerializer,
            }
        ),
    retrieve=extend_schema(
            summary=_("Получить экземпляр связанного адреса по ID (доступно только для администрации сайта)"),
        ),
    update=extend_schema(
        summary=_("Изменение существующего связанного адреса (доступно только для администрации сайта"),
    ),
    partial_update=extend_schema(
        summary=_("Изменение существующего связанного адреса (доступно только для администрации сайта"),
    ),
    destroy=extend_schema(
            summary=_("Удаление существующего связанного адреса (доступно только для администрации сайта"),
        ),
)
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
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список производителей"),
        ),
    retrieve=extend_schema(
            summary=_("Получить экземпляр производителя по ID"),
        ),
    create=extend_schema(
        summary=_("Создать нового производителя (доступно только для администрации сайта)")
    ),
    update=extend_schema(
        summary=_("Изменение существующего производителя (доступно только для администрации сайта"),
    ),
    partial_update=extend_schema(
        summary=_("Изменение существующего производителя (доступно только для администрации сайта"),
    ),
    destroy=extend_schema(
            summary=_("Удаление существующего производителя (доступно только для администрации сайта"),
        ),
)
class APIBrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = BrandFilter


@permission_classes((IsAdminUser,))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить существующие корзины (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить выбранную корзину по ID (доступно только для администрации сайта)"),
        ),
    destroy=extend_schema(
            summary=_("Удалить выбранную корзину (доступно только для администрации сайта)")
        ),
)
class APICartViewSet(ReadDestroyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializerRaw
    pagination_class = StandardResultsSetPagination


@permission_classes((IsAdminUser,))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить текущие позиции в корзинах (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить выбранную позицию из корзин по ID (доступно только для администрации сайта)"),
        ),
    create=extend_schema(
        summary=_("Создание новой позиции в корзине (доступно только для администрации сайта)"),
    ),
    update=extend_schema(
        summary=_("Обновить текущую позицию в корзине (доступно только для администрации сайта)")
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущею позицию в корзине (доступно только для администрации сайта)")
    ),
    destroy=extend_schema(
            summary=_("Удалить текущую позицию в корзине (доступно только для администрации сайта)")
        ),
)
class APICartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = StandardResultsSetPagination


@permission_classes((IsAdminUser, ))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить существующие заказы (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить выбранный заказ по ID (доступно только для администрации сайта)"),
        ),
)
class APIOrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrderFilter
    search_fields = ('order_content', )


@permission_classes((IsAdminUser, ))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список персональных данных (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить персональные данные по ID (доступно только для администрации сайта)"),
        ),
    update=extend_schema(
        summary=_("Обновить текущие персональные данные (доступно только для администрации сайта)")
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущие персональные данные (доступно только для администрации сайта)")
    ),
    destroy=extend_schema(
            summary=_("Удалить текущие персональные данные (доступно только для администрации сайта)")
        ),
)
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
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить текущие публикации на форуме"),
        ),
    retrieve=extend_schema(
            summary=_("Получить выбранную позицию из публикаций по ID"),
        ),
    create=extend_schema(
        summary=_("Создание новой публикации на форуме (доступно только для авторизованного пользователя)"),
    ),
    update=extend_schema(
        summary=_("Обновить текущий пост на форуме (доступно для администрации сайта и автора публикации)")
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущий пост на форуме (доступно для администрации сайта и автора публикации)")
    ),
    destroy=extend_schema(
            summary=_("Удалить текущий пост на форуме (доступно для администрации сайта и автора публикации)")
        ),
)
class APIPostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerRaw
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@permission_classes((IsAdminOrReadOnly,))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить текущие продукты"),
        ),
    retrieve=extend_schema(
            summary=_("Получить выбранный продукт по ID"),
        ),
    update=extend_schema(
        summary=_("Обновить текущий продукт (доступно только для администрации сайта)")
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущий продукт (доступно только для администрации сайта)")
    ),
)
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
@extend_schema_view(
    get=extend_schema(
            summary=_(
                "Получить детализацию выбранного продукта с зависимостями (доступно только для администрации сайта)"),
        ),
    delete=extend_schema(
            summary=_("Удалить выбранный продукт (доступно только для администрации сайта)"),
        ),
)
class APIProductView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


@permission_classes((IsAdminUser,))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список существующих категорий (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить категорию по ID (доступно только для администрации сайта)"),
        ),
    create=extend_schema(
        summary=_("Создание новой категории (доступно только для администрации сайта)"),
    ),
    update=extend_schema(
        summary=_("Обновить выбранную категорию (доступно только для администрации сайта)")
    ),
    partial_update=extend_schema(
        summary=_("Обновить выбранную категорию (доступно только для администрации сайта)")
    ),
    destroy=extend_schema(
            summary=_("Удалить выбранную категорию (доступно только для администрации сайта)")
        ),
)
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
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список таблиц движения товаров (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить выбранную таблицу движения товаров по ID (доступно только для администрации сайта)"),
        ),
)
class APISaleInformationViewSet(ReadOnlyModelViewSet):
    queryset = Sale_information.objects.all()
    serializer_class = SaleInformationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SaleInformationFilter
    search_fields = ('product__title', )


@permission_classes((IsAdminUser, ))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список существующих пользователей (доступно только для администрации сайта)"),
        ),
    retrieve=extend_schema(
            summary=_("Получить пользователя по ID (доступно только для администрации сайта)"),
        ),
    create=extend_schema(
        summary=_("Создание нового пользователя (доступно только для администрации сайта)"),
    ),
    update=extend_schema(
        summary=_("Обновить выбранного пользователя (доступно только для администрации сайта)")
    ),
    partial_update=extend_schema(
        summary=_("Обновить выбранного пользователя (доступно только для администрации сайта)")
    ),
    destroy=extend_schema(
            summary=_("Удалить выбранного пользователя (доступно только для администрации сайта)")
        ),
)
class APIUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = UserFilter


@permission_classes((IsAdminUser, ))
@extend_schema_view(
    get=extend_schema(
            summary=_(
                "Детализация пользователя по ID с имеющимися зависимостями (доступно только для администрации сайта)"),
        ),
    delete=extend_schema(
            summary=_("Удалить выбранного пользователя (доступно только для администрации сайта)")
        ),
)
class APIUserView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


@permission_classes((IsAdminOrReadOnly,))
@extend_schema_view(
    list=extend_schema(
            summary=_("Получить список отзывов и оценок товаров"),
        ),
    retrieve=extend_schema(
            summary=_("выбрать отзыв о товаре по ID"),
        ),
)
class APIVoteViewSet(ReadOnlyModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = VoteFilter
    search_fields = ('review', 'name')
