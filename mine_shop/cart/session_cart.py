import json
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from orders.inner_functions import _separator_normalize
from store.models import Product


class SessionCart(object):
    def __init__(self, request):

        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавить новую позицию или изменить количество в ранее добавленной"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = min(quantity, product.quantity)
        else:
            self.cart[product_id]['quantity'] = min(self.cart[product_id]['quantity'] + quantity, product.quantity)
        if self.cart[product_id]['quantity'] == 0:
            del self.cart[product_id]
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине"""

        for key, item in sorted(self.cart.items()):
            item['total_price'] = str(Decimal(item['price']) * item['quantity'])
            item['product_id'] = key
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(_separator_normalize(item['price'])) * item['quantity'] for item in self.cart.values())

    @property
    def total_count(self):
        return len(self)

    def clear(self):
        """Удаление всей корзины из сессии"""
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def actualize(self):
        for item in self:
            product_id = item['product_id']
            product = get_object_or_404(Product, id=product_id)
            item['quantity'] = min(item['quantity'], product.quantity)
            item['total_price'] = str(Decimal(_separator_normalize(item['price'])) * item['quantity'])
        self.save()

    def serialize(self):
        to_serialize = []
        for item in self:
            to_serialize.append({'id': item['product_id'], 'price': str(item['price']), 'quantity': item['quantity']})
        return json.dumps(to_serialize)
