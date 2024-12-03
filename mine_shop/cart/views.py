from django.shortcuts import render
from siteajax.decorators import ajax_dispatch

from cart.inner_functions import get_current_cart
from mine_shop.ajax_maps import ajax_show_basket_header_map, ajax_show_wishcompare_header_map


@ajax_dispatch(ajax_show_basket_header_map|ajax_show_wishcompare_header_map)
def cart(request):
    cart = get_current_cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart.html', context)
