from django.urls import path

from cart.views import cart

app_name = 'cart'


urlpatterns = [
    path('', cart, name="cart"),
]
