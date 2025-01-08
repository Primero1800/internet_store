import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from siteajax.decorators import ajax_dispatch
from django.utils.translation import gettext as _

from cart.inner_functions import get_current_cart
from mine_shop.ajax_maps import ajax_show_basket_header_map, ajax_show_wishcompare_header_map, \
    ajax_orders_view_total_map
from orders.forms import OrderInformationForm
from orders.inner_functions import get_current_person, get_current_address, get_complex_phonenumber, \
    _separator_normalize
from orders.models import Order, Address, Person
from posts.inner_functions import get_verbose_name
from store.models import Product


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map | ajax_orders_view_total_map)
def orders(request):
    context, cart = {}, None
    if request.method == 'POST':
        form = OrderInformationForm(data=request.POST)

        if form.is_valid():
            person = get_current_person(request)
            address = get_current_address(request)
            complex_phonenumber = get_complex_phonenumber(request.POST['phonenumber_0'], request.POST['phonenumber_1'])
            person.set_attributes(request.POST['name'], request.POST['surname'], request.POST['company_name'])
            address.set_attributes(
                request.POST['address'], request.POST['city'], request.POST['postcode'],
                request.POST['email'], complex_phonenumber
            )

            total_price = Decimal(_separator_normalize(request.POST['total_price']))
            cart = get_current_cart(request)
            if total_price != cart.total_price:
                context['message'] = _("Во время заполнения данных заказа Ваша корзина претерпела изменения. Проверьте данные.")
            else:
                json_cart = cart.serialize()
                json_person = person.serialize()
                json_address = address.serialize()
                order = Order(
                    phonenumber=address.get_phonenumber(),
                    order_content=json_cart,
                    person_content=json_person,
                    address_content=json_address,
                    total_price=cart.total_price,
                )
                user = request.user
                if user.is_authenticated:
                    order.user = user
                delivery = request.POST['delivery']
                payment = request.POST['payment']
                if delivery == 'yes':
                    order.move_to = Order.MovingChoices.place_1
                if payment == 'card':
                    order.payment_conditions = Order.PaymentChoices.payment_2
                elif payment == 'cash':
                    order.payment_conditions = Order.PaymentChoices.payment_3

                order.reserve()
                order.save()
                cart.clear()

                response = HttpResponseRedirect(redirect_to=reverse('orders:history', args=('success',)))
                response.set_cookie('last_order_id', order.pk)
                return response

    else:
        person = get_current_person(request)
        address = get_current_address(request)
        data = person.to_form() | address.to_form()
        form = OrderInformationForm(data=data)

    if not cart:
        cart = get_current_cart(request)
    cart.actualize()

    context['form'] = form
    context['cart'] = cart
    context['total_price'] = cart.total_price
    return render(request, 'orders/orders.html', context)


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def orders_history(request, success=None):

    context, order_id = {}, None
    orders_info = []

    if success:
        try:
            order_id = int(request.COOKIES['last_order_id'])
            d = 2
        except KeyError:
            return HttpResponseRedirect(reverse('store:error', args=(1,)))

        order = get_object_or_404(Order, id=order_id)

        context['new_order'] = {
            'address': json.loads(order.address_content),
            'time_placed': order.time_placed,
            'status': order.status,
            'id': order.pk,
            'payment_conditions': order.payment_conditions,
            'total_price': order.total_price
        }
        raw_products = json.loads(order.order_content)
        products = []
        for product in raw_products:
            prod = get_object_or_404(Product, id=product['id'])
            product['title'] = prod.title
            product['slug'] = prod.slug
            product['image_url'] = prod.images.first().image.url
            products.append(product)
        context['new_order']['products'] = products

    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(user=user)
        for order in orders:
            item = {}
            item['address'] = json.loads(order.address_content)
            item['time_placed'] = order.time_placed
            item['time_delivered'] = order.time_delivered
            item['status'] = order.status
            item['id'] = order.pk
            item['payment_conditions'] = order.payment_conditions
            item['total_price'] = order.total_price
            raw_products = json.loads(order.order_content)
            products = []
            for product in raw_products:
                prod= get_object_or_404(Product, id=product['id'])
                product['title'] = prod.title
                product['slug'] = prod.slug
                product['image_url'] = prod.images.first().image.url
                products.append(product)
            item['products'] = products

            if order_id != item['id']:
                orders_info.append(item)

        context['orders'] = orders_info

    response = render(request, 'orders/orders_history.html', context)
    response.delete_cookie('last_order_id')
    return response


@login_required(login_url=reverse_lazy("users:login"), redirect_field_name='next')
@ajax_dispatch(ajax_orders_view_total_map)
def admin_orders(request):
    user = request.user
    if not user.is_staff or not user.is_superuser:
        return HttpResponseRedirect(reverse('store:error', args=(1, )))

    context = {}
    orders = Order.objects.all()
    delivered = orders.filter(status=1)
    last_delivered = delivered.order_by('time_delivered').last()
    awaits = orders.filter(status=0)
    long_await = awaits.order_by('time_placed').first()
    cancelled = orders.filter(status=2)

    context['orders_info'] = {
        'count': {
            'all': len(orders),
            'delivered': len(delivered),
            'awaits': len(awaits),
            'cancelled': len(cancelled),
        },
        'last_delivery': {
            'id': None if not last_delivered else last_delivered.id,
            'time_delivered': None if not last_delivered else last_delivered.time_delivered,
        },
        'long_await': {
            'id': None if not long_await else long_await.id,
            'time_placed': None if not long_await else long_await.time_placed,
        },
    }
    context['order_fields'] = {
        'time_placed': get_verbose_name(Order, 'time_placed'),
        'status': get_verbose_name(Order, 'status'),
        'time_delivered': get_verbose_name(Order, 'time_delivered'),
        'total_price': get_verbose_name(Order, 'total_price'),
        'payment_conditions': get_verbose_name(Order, 'payment_conditions'),
        'address': get_verbose_name(Address, 'address'),
        'person': get_verbose_name(Person, 'name'),
        'user': get_verbose_name(Order, 'user'),
    }

    return render(request, 'orders/admin_orders.html', context)


def proceed_order(request):
    if request.method == 'POST':
        order_id = int(request.POST['order_id'])
        order = get_object_or_404(Order, id=order_id)
        if order.status == 0:
            if 'delivery' in request.POST:
                order.deliver()
            else:
                order.cancel_reserve()

        if 'admin' in request.POST:
            return HttpResponseRedirect(reverse('orders:admin_orders'))
        elif request.user.is_authenticated:
            return HttpResponseRedirect(reverse('orders:history'))
        else:
            return HttpResponseRedirect(reverse('orders:orders_message'))

    return HttpResponseRedirect(reverse('store:index'))


def orders_message(request):
    return render(request, 'orders/orders_message.html', {})
