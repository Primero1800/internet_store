from django.conf import settings
from django.shortcuts import get_object_or_404

from cart.models import Cart
from cart.session_cart import SessionCart
from store.models import Product


def get_current_cart(request):
    user = request.user
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
    else:
        cart = SessionCart(request)
    return cart


def ajax_cart_remove(cart, kwargs):
    product_id = int(kwargs['product_id'][0]) if 'product_id' in kwargs else None
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)


def ajax_cart_add(cart, quantity, kwargs):
    product_id = int(kwargs['product_id'][0]) if 'product_id' in kwargs else None
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity, update_quantity=False)


def is_product_in_cart(product=None, product_id=None, cart=None):
    if not cart or (not product and not product_id):
        return False

    if isinstance(cart, dict):
        product_id = str(product.id) if product else str(product_id)
        return product_id in cart

    else:  # cart is Cart
        product_id = int(product_id) if not product else product.id
        return len(cart.cart_items.filter(product__id=product_id)) > 0


def get_delivery_cost(total_count):
    return settings.ORDERS_DELIVERY_COST if total_count < settings.ORDERS_FREE_DELIVERY_FLOOR else 0
