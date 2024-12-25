from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('users/', include('users.urls', namespace='users')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('api/v1/', include('api.urls', namespace='v1')),
    path(f'api-auth/', include("rest_framework.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
