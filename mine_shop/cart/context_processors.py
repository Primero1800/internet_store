from cart.inner_functions import get_current_cart


def add_cart_to_context(request):
    return {'cart': get_current_cart(request)}