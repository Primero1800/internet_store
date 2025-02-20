from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.decorators import permission_classes
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from cart.models import Cart, CartItem
from .filters import (
    AddressFilter, BrandFilter, OrderFilter, PersonFilter, PostFilter, ProductFilter,
    RubricFilter, SaleInformationFilter, UserFilter, VoteFilter
)
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
    PersonSerializer, PostSerializerRaw, ProductSerializerRaw, RubricSerializerRaw, ApiErrorSerializer
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
        parameters=[
            OpenApiParameter(name='city', description='Filter city =',),
            OpenApiParameter(name='id', description='Filter id =',),
            OpenApiParameter(name='id__gte', description='Filter id >=',),
            OpenApiParameter(name='id__lte', description='Filter id <=',),
            OpenApiParameter(name='phonenumber', description='Filter phonenumber =',),
            OpenApiParameter(name='phonenumber__contains', description='Filter phonumber__contains',),
            OpenApiParameter(name='user', description='Filter user =',),
        ],
        responses={
            status.HTTP_200_OK: AddressSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        }
    ),
    retrieve=extend_schema(
        summary=_("Получить экземпляр связанного адреса по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: AddressSerializerRaw,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
    ),
    update=extend_schema(
        summary=_("Изменение существующего связанного адреса (доступно только для администрации сайта"),
        responses={
            status.HTTP_200_OK: AddressSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
    ),
    partial_update=extend_schema(
        summary=_("Изменение существующего связанного адреса (доступно только для администрации сайта"),
        responses={
            status.HTTP_200_OK: AddressSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
    ),
    destroy=extend_schema(
        summary=_("Удаление существующего связанного адреса (доступно только для администрации сайта"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
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
        parameters=[
            OpenApiParameter(name='id', description='Filter id =',),
            OpenApiParameter(name='items', description='Filter items in',),
            OpenApiParameter(name='title', description='Filter title =',),
            OpenApiParameter(name='title__contains', description='Filter title__contains',),
        ],
        responses={
            status.HTTP_200_OK: BrandSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить экземпляр производителя по ID"),
        responses={
            status.HTTP_200_OK: BrandSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
    ),
    create=extend_schema(
        summary=_("Создать нового производителя (доступно только для администрации сайта)"),
        responses={
            status.HTTP_201_CREATED: BrandSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        }
    ),
    update=extend_schema(
        summary=_("Изменение существующего производителя (доступно только для администрации сайта"),
        responses={
            status.HTTP_200_OK: BrandSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
    ),
    partial_update=extend_schema(
        summary=_("Изменение существующего производителя (доступно только для администрации сайта"),
        responses={
            status.HTTP_200_OK: BrandSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
    ),
    destroy=extend_schema(
        summary=_("Удаление существующего производителя (доступно только для администрации сайта"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
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
        responses={
            status.HTTP_200_OK: CartSerializerRaw,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить выбранную корзину по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: CartSerializerRaw,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    destroy=extend_schema(
        summary=_("Удалить выбранную корзину (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
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
        responses={
            status.HTTP_200_OK: CartItemSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить выбранную позицию из корзин по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: CartItemSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    create=extend_schema(
        summary=_("Создание новой позиции в корзине (доступно только для администрации сайта)"),
        responses={
            status.HTTP_201_CREATED: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        }
    ),
    update=extend_schema(
        summary=_("Обновить текущую позицию в корзине (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущею позицию в корзине (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: CartItemSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    destroy=extend_schema(
        summary=_("Удалить текущую позицию в корзине (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
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
        parameters=[
            OpenApiParameter(name='phonenumber__contains', description='Filter phonenumber__contains',),
            OpenApiParameter(name='search', description="Search term. Searching in 'order_content'",),
            OpenApiParameter(
                name='time_delivered__range_after', description='Filter time_delivered in range. yyyy-mm-dd',
            ),
            OpenApiParameter(name='time_placed__range_after', description='Filter time_placed in range. yyyy-mm-dd',),
            OpenApiParameter(name='total_price__gte', description='Filter total_price >=',),
            OpenApiParameter(name='total_price__lte', description='Filter total_price <=',),
        ],
        responses={
            status.HTTP_200_OK: OrderSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить выбранный заказ по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: OrderSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
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
        parameters=[
            OpenApiParameter(name='user', description='Filter user =', type=int),
        ],
        responses={
            status.HTTP_200_OK: PersonSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить персональные данные по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: PersonSerializerRaw,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    update=extend_schema(
        summary=_("Обновить текущие персональные данные (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: PersonSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущие персональные данные (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: PersonSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    destroy=extend_schema(
        summary=_("Удалить текущие персональные данные (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        }
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
        parameters=[
            OpenApiParameter(name='id', description='Filter id =', type=int),
            OpenApiParameter(name='product', description="Filter product =", type=int),
            OpenApiParameter(name='user', description='Filter user=', type=int),
        ],
        responses={
            status.HTTP_200_OK: PostSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить выбранную позицию из публикаций по ID"),
        responses={
            status.HTTP_200_OK: PostSerializerRaw,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    create=extend_schema(
        summary=_("Создание новой публикации на форуме (доступно только для авторизованного пользователя)"),
        responses={
            status.HTTP_201_CREATED: PostSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        }
    ),
    update=extend_schema(
        summary=_("Обновить текущий пост на форуме (доступно для администрации сайта и автора публикации)"),
        responses={
            status.HTTP_200_OK: PostSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущий пост на форуме (доступно для администрации сайта и автора публикации)"),
        responses={
            status.HTTP_200_OK: PostSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    destroy=extend_schema(
        summary=_("Удалить текущий пост на форуме (доступно для администрации сайта и автора публикации)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
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
        parameters=[
            OpenApiParameter(name='brand', description='Filter brand =', type=int),
            OpenApiParameter(name='discont__gte', description="Filter discont >=", type=int),
            OpenApiParameter(name='quantity__lte', description="Filter quantity <=", type=int),
            OpenApiParameter(name='search', description='Search term. Searching in title and description', ),
            OpenApiParameter(name='title__contains', description='Filter title__contains',),
            OpenApiParameter(
                name='rubrics', description='Filter by rubrics',
                type={'type': 'array', 'items': {'type': 'integer'}},
                location=OpenApiParameter.QUERY,
                style='form',
            ),
        ],
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить выбранный продукт по ID"),
        responses={
            status.HTTP_200_OK: ProductSerializerRaw,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    update=extend_schema(
        summary=_("Обновить текущий продукт (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: ProductSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    partial_update=extend_schema(
        summary=_("Обновить текущий продукт (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: ProductSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
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
        responses={
            status.HTTP_200_OK: ProductDetailSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
        ),
    delete=extend_schema(
        summary=_("Удалить выбранный продукт (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
)
class APIProductView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


@permission_classes((IsAdminOrReadOnly,))
@extend_schema_view(
    list=extend_schema(
        summary=_("Получить список существующих категорий (доступно только для администрации сайта)"),
        parameters=[
            OpenApiParameter(
                name='products', description='Filter by products',
                type={'type': 'array', 'items': {'type': 'integer'}},
                location=OpenApiParameter.QUERY,
                style='form',
            ),
        ],
        responses={
            status.HTTP_200_OK: RubricSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить категорию по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    create=extend_schema(
        summary=_("Создание новой категории (доступно только для администрации сайта)"),
        responses={
            status.HTTP_201_CREATED: RubricSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        }
    ),
    update=extend_schema(
        summary=_("Обновить выбранную категорию (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: RubricSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    partial_update=extend_schema(
        summary=_("Обновить выбранную категорию (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: RubricSerializerRaw,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    destroy=extend_schema(
        summary=_("Удалить выбранную категорию (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
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
        parameters=[
            OpenApiParameter(name='calculated_rating__gte', description='Filter rating >=', type=float),
            OpenApiParameter(name='calculated_rating__lte', description="Filter rating <=", type=float),
            OpenApiParameter(name='search', description='Search term. Searching in title of product', ),
            OpenApiParameter(name='sold_count__gte', description='Filter sold_count >=', type=int),
            OpenApiParameter(name='sold_count__lte', description="Filter sold_count <=", type=int),
            OpenApiParameter(name='viewed_count__gte', description='Filter viewed_count >=', type=int),
            OpenApiParameter(name='viewed_count__lte', description="Filter viewed_count <=", type=int),
        ],
        responses={
            status.HTTP_200_OK: SaleInformationSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить выбранную таблицу движения товаров по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: SaleInformationSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
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
        parameters=[
            OpenApiParameter(name='email__contains', description='Filter email__contains',),
            OpenApiParameter(name='is_active', description="Filter is_active =", type=bool),
            OpenApiParameter(name='is_staff', description="Filter is_staff =", type=bool),
            OpenApiParameter(name='is_superuser', description="Filter is_superuser =", type=bool),
        ],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("Получить пользователя по ID (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    create=extend_schema(
        summary=_("Создание нового пользователя (доступно только для администрации сайта)"),
        responses={
            status.HTTP_201_CREATED: UserSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        }
    ),
    update=extend_schema(
        summary=_("Обновить выбранного пользователя (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    partial_update=extend_schema(
        summary=_("Обновить выбранного пользователя (доступно только для администрации сайта)"),
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
    destroy=extend_schema(
        summary=_("Удалить выбранного пользователя (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
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
        summary=_("Удалить выбранного пользователя (доступно только для администрации сайта)"),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_403_FORBIDDEN: ApiErrorSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
)
class APIUserView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


@permission_classes((IsAdminOrReadOnly,))
@extend_schema_view(
    list=extend_schema(
        summary=_("Получить список отзывов и оценок товаров"),
        parameters=[
            OpenApiParameter(name='product', description='Filter product =', type=int),
            OpenApiParameter(name='search', description='Search term. Searching in review and name'),
            OpenApiParameter(name='stars__gte', description="Filter stars >=", type=float),
            OpenApiParameter(name='stars__lte', description="Filter stars <= =", type=float),
            OpenApiParameter(name='user', description="Filter user =", type=int),
            OpenApiParameter(
                name='time_published__range_after', description='Filter time_published in range. yyyy-mm-dd',
            ),
        ],
        responses={
            status.HTTP_200_OK: VoteSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        },
    ),
    retrieve=extend_schema(
        summary=_("выбрать отзыв о товаре по ID"),
        responses={
            status.HTTP_200_OK: VoteSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
        },
    ),
)
class APIVoteViewSet(ReadOnlyModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = VoteFilter
    search_fields = ('review', 'name')
