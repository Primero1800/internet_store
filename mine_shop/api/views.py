from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart
from orders.models import Person, Address, Order
from posts.models import Post
from store.info_classes import Vote, Sale_information
from store.models import Product, Brand, Rubric
from users.models import User
from .serializers import UserSerializer, UserDetailSerializer, PersonSerializer, AddressSerializer, CartSerializer, \
    PostSerializer, VoteSerializer, OrderSerializer, ProductSerializer, BrandSerializer, RubricSerializer, \
    SaleInformationSerializer, ProductDetailSerializer


@permission_classes((IsAdminUser, ))
class APIUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((IsAdminUser, ))
class APIPersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@permission_classes((IsAdminUser, ))
class APIAddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


@permission_classes((IsAdminUser,))
class APICartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


@permission_classes((IsAdminUser,))
class APIPostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@permission_classes((IsAdminUser,))
class APIVoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

@permission_classes((IsAdminUser,))
class APIBrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

@permission_classes((IsAdminUser,))
class APISaleInformationViewSet(ModelViewSet):
    queryset = Sale_information.objects.all()
    serializer_class = SaleInformationSerializer

@permission_classes((IsAdminUser,))
class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer

@permission_classes((IsAdminUser,))
class APIOrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@permission_classes((IsAdminUser,))
class APIProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@permission_classes((IsAdminUser, ))
class APIUserView(RetrieveAPIView, DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


@permission_classes((IsAdminUser, ))
class APIProductView(RetrieveAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
