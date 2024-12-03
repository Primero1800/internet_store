from django.shortcuts import render
from siteajax.decorators import ajax_dispatch

from mine_shop.ajax_maps import ajax_show_basket_header_map, ajax_show_wishcompare_header_map, ajax_show_posts_map


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map | ajax_show_posts_map)
def index(request):
    context = {}
    return render(request, 'posts/forum.html', context)


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def information(request):
    context = {}
    return render(request, 'posts/information.html', context)
