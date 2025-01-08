from django.shortcuts import render, get_object_or_404
from siteajax.utils import AjaxResponse

from store.models import Product
from users.inner_functions import get_products_by_tool_items
from users.models import UserTools


def ajax_show_wishcompare_header(request, *args, **kwargs):
    context = {}
    user = request.user
    params = dict(request.POST) if request.method == 'POST' else dict(request.GET)

    if user.is_authenticated:
        usertools, _ = UserTools.objects.get_or_create(user=user)

        if 'value' in params and 'product_id' in params:
            value = params['value'][0]
            product_id = int(params['product_id'][0])
            product = get_object_or_404(Product, id=product_id)
            if product:
                if value == 'w':
                    usertools.add_w(product)
                elif value == 'c':
                    usertools.add_c(product)

        context['c_count'] = usertools.total_count_c
        context['w_count'] = usertools.total_count_w

    return AjaxResponse(render(request, 'users/ajax_divs/ajax_div_wishcompare.html', context))


def ajax_show_wishlist_content(request, *args, **kwargs):
    usertools, _ = UserTools.objects.get_or_create(user=request.user)
    context = {}

    if request.ajax.source.id.startswith('wishlist-item-delete'):
        params = dict(request.POST) if request.method == 'POST' else dict(request.GET)
        product_id = int(params['product_id'][0]) if 'product_id' in params else None
        if product_id:
            usertools.w_items.filter(product_id=product_id).delete()
            context['wc_updated'] = True
    context['products'] = get_products_by_tool_items(usertools.w_items.all())

    return AjaxResponse(render(request, 'users/ajax_divs/ajax_div_wishlist_content.html', context))


def ajax_show_comparison_content(request, *args, **kwargs):
    usertools, _ = UserTools.objects.get_or_create(user=request.user)
    context = {}

    if request.ajax.source.id.startswith('comparison-item-delete'):
        params = dict(request.POST) if request.method == 'POST' else dict(request.GET)
        product_id = int(params['product_id'][0]) if 'product_id' in params else None
        if product_id:
            usertools.c_items.filter(product_id=product_id).delete()
            context['wc_updated'] = True
    context['products'] = get_products_by_tool_items(usertools.c_items.all())

    return AjaxResponse(render(request, 'users/ajax_divs/ajax_div_comparison_content.html', context))
