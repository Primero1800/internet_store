from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import APIUserViewSet, APIUserView, APIPersonViewSet, APIAddressViewSet, APICartViewSet, APIPostViewSet, \
    APIVoteViewSet, APIOrderViewSet, APIProductViewSet, APIBrandViewSet, APIRubricViewSet, APISaleInformationViewSet, \
    APIProductView

app_name = 'api'

router = DefaultRouter()

router.register('users', APIUserViewSet)
router.register('products', APIProductViewSet)
router.register('persons', APIPersonViewSet)
router.register('adresses', APIAddressViewSet)
router.register('carts', APICartViewSet)
router.register('posts', APIPostViewSet)
router.register('votes', APIVoteViewSet)
router.register('orders', APIOrderViewSet)
router.register('brands', APIBrandViewSet)
router.register('rubrics', APIRubricViewSet)
router.register('sale_information', APISaleInformationViewSet)


urlpatterns = [

    path('users/<int:pk>/detail/', APIUserView.as_view(), name='user_detail'),
    path('products/<int:pk>/detail/', APIProductView.as_view(), name='product_detail'),
    path('', include(router.urls)),





    # path('admin/full/<sort_by>/<count>/', products_full, name="products_full"),
    # path('admin/full/<sort_by>/', products_full, name="products_full"),
    # path('admin/full/<count>/', products_full, name="products_full"),
    # path('admin/full/', products_full, name="products_full"),
    #
    # path('admin/user_detail/<int:pk>/', UserDetailView.as_view(), name='user_details'),
    #
    # path('admin/user/<int:pk>/', APIUserDetailView.as_view(), name='simple_user'),
    # path('admin/user/', APIUserView.as_view(), name='simple_user'),
    #
    # path('admin/users/<sort_by>/<count>/', users, name="products_full"),
    # path('admin/users/<sort_by>/', users, name="products_full"),
    # path('admin/users/<count>/', users, name="products_full"),
    # path('admin/users/', users, name="users"),
    #
    # path('admin/orders/<sort_by>/<count>/', orders, name='orders'),
    # path('admin/orders/<sort_by>/', orders, name='orders'),
    # path('admin/orders/<count>/', orders, name='orders'),
    # path('admin/orders/', orders, name='orders'),
    #
    # path('admin/detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    #
    # path('admin/<sort_by>/<str:count>/', products_short, name="products_short"),
    # path('admin/<sort_by>/', products_short, name="products_short"),
    # path('admin/<str:count>/', products_short, name="products_short"),
    # path('admin/', products_short, name="products_short"),
    #
    # path('detail/<int:pk>/', ProductDetailFreeView.as_view(), name='detail'),
    #
    # path('<sort_by>/<str:count>/', products_short_free, name="products_short"),
    # path('<sort_by>/', products_short_free, name="products_short"),
    # path('<str:count>/', products_short_free, name="products_short"),
    # path('', products_short_free, name="products_short"),

]