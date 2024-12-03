from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404

from cart.session_cart import SessionCart
from store.models import Product
from users.models import User

from django.utils.translation import gettext as _
from decimal import Decimal
import json


class Cart(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_("Покупатель"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата и время создания"))

    class Meta:
        verbose_name = _("Корзина")

    @property
    def total_price(self):
        total_price = sum(item.total_price for item in self.cart_items.all())
        return total_price

    @property
    def total_count(self):
        return sum(item.quantity for item in self.cart_items.all())

    def __iter__(self):
        yield from self.cart_items.all().order_by('product_id')

    def clear(self):
        self.cart_items.all().delete()


    def add(self, product, quantity=1, update_quantity=False):
        try:
            item = self.cart_items.get(product=product)
        except:
            item = CartItem(cart=self, product=product, price=product.price, quantity=0)
        if update_quantity:
            item.quantity = min(quantity, product.quantity)
        else:
            item.quantity = min(item.quantity + quantity, product.quantity)
        item.save()
        if item.quantity == 0:
            self.cart_items.filter(id=item.id).delete()
        self.save()


    def remove(self, product):
        self.cart_items.filter(product=product).delete()

    def __add__(self, other):
        if settings.GLOBAL_CART_PREFERENCES == '0':
            if isinstance(other, SessionCart):
                for item in other:
                    product = get_object_or_404(Product, id=int(item['product_id']))
                    if product:
                        self.add(product=product, quantity=item['quantity'], update_quantity=False)
            elif isinstance(other, Cart):
                for item in other:
                    self.add(product=item.product, quantity=item.quantity, update_quantity=False)
            else:
                return self
            self.save()
        other.clear()
        return self


    def __iadd__(self, other):
        return self + other


    def actualize(self):
        for item in self:
            item.actualize_item()


    def serialize(self):
        to_serialize = []
        for item in self:
            to_serialize.append({'id': item.product.id, 'price': str(item.price), 'quantity': item.quantity})
        return json.dumps(to_serialize)


class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='cart_items', verbose_name=_("Корзина"))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_("Продукт"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    quantity = models.PositiveIntegerField(verbose_name=_("Количество"))

    class Meta:
        verbose_name = _("Товар в корзине")
        verbose_name_plural = _("Товары в корзине")

    @property
    def total_price(self):
        return Decimal(self.price * self.quantity)

    def actualize_item(self):
        self.quantity = min(self.quantity, self.product.quantity)
        self.save()

