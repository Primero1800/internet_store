from django.shortcuts import render
from siteajax.utils import AjaxResponse

from cart.inner_functions import get_current_cart, ajax_cart_remove, ajax_cart_add


def ajax_show_basket_in_header(request, *args, **kwargs):
    cart = get_current_cart(request)
    params = dict(request.POST)

    if request.ajax.source.id.startswith('add-cart-button'):
        quantity = 1
        ajax_cart_add(cart, quantity, params)

    elif request.ajax.source.id == 'remove-cart-button':
        ajax_cart_remove(cart, params)

    elif request.ajax.source.id == 'add_quantity_cart_button':
        quantity = int(params['add_quantity'][0])
        ajax_cart_add(cart, quantity, params)

    response = AjaxResponse(render(request, 'cart/ajax_divs/ajax_div_basket.html', {}))
    return response


def ajax_show_basket_content(request):
    cart = get_current_cart(request)

    if request.ajax.source.id != 'basket-content':
        params = dict(request.POST)

        if request.ajax.source.id == 'remove-cart-button-content':
            ajax_cart_remove(cart, params)

        elif request.ajax.source.id.startswith('cart-item-quantity'):
            quantity = -1 if request.ajax.source.id.endswith('0') else 1
            ajax_cart_add(cart, quantity, params)

    response = AjaxResponse(render(request, 'cart/ajax_divs/ajax_div_basket_content.html', {}))
    return response
