from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import APIUserViewSet, APIUserView, APIPersonViewSet, APIAddressViewSet, APICartViewSet, APIPostViewSet, \
    APIVoteViewSet, APIOrderViewSet, APIProductViewSet, APIBrandViewSet, APIRubricViewSet, APISaleInformationViewSet, \
    APIProductView, APICartItemViewSet

app_name = 'v1'

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

    path(f'products/<int:pk>/detail/', APIProductView.as_view(), name='product_detail'),
    path(f'users/<int:pk>/detail/', APIUserView.as_view(), name='user_detail'),
    path(f'', include(router.urls)),

]


