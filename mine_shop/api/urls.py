from django.urls import path

from .views import (
    products_short, products_full, ProductDetailView, products_short_free, ProductDetailFreeView, orders, users, UserDetailView
)

app_name = 'api'


urlpatterns = [

    path('admin/full/<sort_by>/<count>/', products_full, name="products_full"),
    path('admin/full/<sort_by>/', products_full, name="products_full"),
    path('admin/full/<count>/', products_full, name="products_full"),
    path('admin/full/', products_full, name="products_full"),

    path('admin/user_detail/<int:pk>/', UserDetailView.as_view(), name='user_details'),

    path('admin/users/<sort_by>/<count>/', users, name="products_full"),
    path('admin/users/<sort_by>/', users, name="products_full"),
    path('admin/users/<count>/', users, name="products_full"),
    path('admin/users/', users, name="users"),

    path('admin/orders/<sort_by>/<count>/', orders, name='orders'),
    path('admin/orders/<sort_by>/', orders, name='orders'),
    path('admin/orders/<count>/', orders, name='orders'),
    path('admin/orders/', orders, name='orders'),

    path('admin/detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),

    path('admin/<sort_by>/<str:count>/', products_short, name="products_short"),
    path('admin/<sort_by>/', products_short, name="products_short"),
    path('admin/<str:count>/', products_short, name="products_short"),
    path('admin/', products_short, name="products_short"),

    path('detail/<int:pk>/', ProductDetailFreeView.as_view(), name='detail'),

    path('<sort_by>/<str:count>/', products_short_free, name="products_short"),
    path('<sort_by>/', products_short_free, name="products_short"),
    path('<str:count>/', products_short_free, name="products_short"),
    path('', products_short_free, name="products_short"),

]