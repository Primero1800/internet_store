from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import APIUserViewSet, APIUserView, APIPersonViewSet, APIAddressViewSet, APICartViewSet, APIPostViewSet, \
    APIVoteViewSet, APIOrderViewSet, APIProductViewSet, APIBrandViewSet, APIRubricViewSet, APISaleInformationViewSet, \
    APIProductView, APIAddressView, APICartView, APICartItemViewSet, APIPersonView

app_name = 'api'
VERSION = 'v1'

router = DefaultRouter()

router.register('addresses', APIAddressViewSet)
router.register('brands', APIBrandViewSet)
router.register('carts', APICartViewSet)
router.register('cartitems', APICartItemViewSet)
router.register('orders', APIOrderViewSet)
router.register('persons', APIPersonViewSet)
router.register('posts', APIPostViewSet)
router.register('products', APIProductViewSet)
router.register('rubrics', APIRubricViewSet)
router.register('sale_information', APISaleInformationViewSet)
router.register('users', APIUserViewSet)
router.register('votes', APIVoteViewSet)

urlpatterns = [

    path(f'{VERSION}/addresses/<int:pk>/', APIAddressView.as_view(), name='address_detail'),
    path(f'{VERSION}/carts/<int:pk>/', APICartView.as_view(), name='cart_detail'),
    path(f'{VERSION}/persons/<int:pk>/', APIPersonView.as_view(), name='person_detail'),
    path(f'{VERSION}/products/<int:pk>/detail/', APIProductView.as_view(), name='product_detail'),
    path(f'{VERSION}/users/<int:pk>/detail/', APIUserView.as_view(), name='user_detail'),
    path(f'{VERSION}/', include(router.urls)),

]
