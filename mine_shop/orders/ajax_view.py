import json

from django.shortcuts import render, get_object_or_404
from siteajax.utils import AjaxResponse

from cart.inner_functions import get_current_cart, get_delivery_cost
from orders.models import Order
from store.models import Product

ORDERS_PER_PAGE = 5


def ajax_orders_view_total(request, *args, **kwargs):
    context = {}
    if request.ajax.source.id == 'total_field':
        cart = get_current_cart(request)
        delivery_cost = get_delivery_cost(cart.total_price)
        order_total_price = cart.total_price + delivery_cost
        context['order_total_price'] = order_total_price

    elif request.ajax.source.id == 'delivery_group':
        delivery = request.POST['delivery']
        if delivery == 'no':
            context['order_total_price'] = get_current_cart(request).total_price
        else:
            cart = get_current_cart(request)
            delivery_cost = get_delivery_cost(cart.total_price)
            order_total_price = cart.total_price + delivery_cost
            context['order_total_price'] = order_total_price

    return AjaxResponse(render(request, 'orders/ajax_divs/ajax_div_total_field.html', context))


def ajax_view_orders(request, *args, **kwargs):
    context = {}

    all_orders = Order.objects.all()
    last_order_id = all_orders.first().id + 1 if 'last_order_id' not in request.POST else request.POST['last_order_id']
    orders = all_orders.filter(id__lt=last_order_id)
    if len(orders) > ORDERS_PER_PAGE:
        context['has_next'] = True
        orders = orders[:ORDERS_PER_PAGE]

    if orders:
        context['last_order_id'] = list(orders)[-1].pk

    orders_info = []

    for order in orders:
        item = {
            'time_placed': order.time_placed,
            'id': order.pk,
            'address': json.loads(order.address_content),
            'person': json.loads(order.person_content),
            'time_delivered': order.time_delivered,
            'status': order.status,
            'total_price': order.total_price,
            'payment_conditions': order.payment_conditions,
            'user': order.user
        }
        raw_products = json.loads(order.order_content)
        products = []
        for product in raw_products:
            product_instance = get_object_or_404(Product, id=product['id'])
            product['title'] = product_instance.title
            product['slug'] = product_instance.slug
            product['image_url'] = product_instance.images.first().image.url
            products.append(product)
        item['products'] = products
        orders_info.append(item)

    context['orders'] = orders_info

    return AjaxResponse(render(request, 'orders/ajax_divs/ajax_div_admin_orders.html', context))