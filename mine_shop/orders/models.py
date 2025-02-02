import asyncio

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone

import json

from posts.inner_functions import send_telegram_message
from store.models import Product
from users.models import User


class Person(models.Model):
    name = models.CharField(max_length=50, error_messages={"required": _("Обязательное условие"), }, verbose_name=_("Имя"))
    surname = models.CharField(
        blank=True, default='', max_length=50,
        error_messages={'max_length': _("Атрибут не может состоять более чем из 50 символов")},
        verbose_name=_("Фамилия")
    )
    company_name = models.CharField(
        blank=True, default='', max_length=100,
        error_messages={
            'max_length': _("Атрибут не может состоять более чем из 50 символов"),
            'min_length': _("Атрибут не может состоять менее чем из 3 символов")
        },
        verbose_name=_("Компания")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))

    class Meta:
        verbose_name = _("Персона")
        ordering = ('id', )

    def set_attributes(self, name=None, surname=None, company_name=None):
        self.name = name
        self.surname = surname
        self.company_name = company_name
        self.save()

    def get_fullname(self):
        return (self.name + ' ' + self.surname).strip()

    def to_form(self):
        return {'name': self.name, 'surname': self.surname, 'company_name': self.company_name}

    def serialize(self):
        to_serialize = {
            'name': self.name,
            'surname': self.surname,
            'company_name': self.company_name
        }
        return json.dumps(to_serialize)


class Address(models.Model):
    address = models.CharField(max_length=150, verbose_name=_("Адрес доставки"))
    city = models.CharField(max_length=50, verbose_name=_("Населенный пункт"))
    postcode = models.IntegerField(blank=True, null=True,  verbose_name=_("Почтовый код"))
    email = models.EmailField(blank=True, max_length=70,
                                  error_messages={'max_length': _("Атрибут не может состоять более чем из 70 символов"),
                                                                    'min_length': _("Атрибут не может состоять менее чем из 3 символов")},
                                  verbose_name=_("Адрес эл.почты"))
    phonenumber = models.CharField(max_length=70, error_messages={'invalid': _("Неверный телефонный номер")},
                           verbose_name=_("Телефонный номер"))

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))

    class Meta:
        verbose_name = _("Адрес")
        ordering = ('id', )

    def get_phonenumber(self):
        return self.phonenumber

    def set_attributes(self, address=None, city=None, postcode=0, email=None, phonenumber=None):
        self.address = address
        self.city = city
        self.postcode = postcode if postcode else 0
        self.email = self.user.email
        self.phonenumber = phonenumber

        self.save()

    def to_form(self):
        phonenumber = self.phonenumber.split(settings.PHONE_NUMBER_DATABASE_SEPARATOR)
        return {
            'address': self.address,
            'city': self.city,
            'postcode': self.postcode,
            'email': self.user.email,
            'phonenumber_0': phonenumber[0],
            'phonenumber_1': phonenumber[-1]
        }

    def serialize(self):
        to_serialize = {
            'address': self.address,
            'city': self.city,
            'postcode': self.postcode,
            'email': self.email,
            'phonenumber': self.phonenumber
        }
        return json.dumps(to_serialize)


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_("Пользователь"))
    phonenumber = models.CharField(max_length=70, error_messages={'invalid': _("Неверный телефонный номер")},
                                                                      verbose_name=_("Телефонный номер"))
    order_content = models.CharField(max_length=2000, error_messages={'invalid': _("Ошибка в заказе")},
                                                                      verbose_name=_("Данные заказа"))
    person_content = models.CharField(max_length=200, error_messages={'invalid': _("Ошибка в данных")},
                                     verbose_name=_("Данные пользователя"))
    address_content = models.CharField(max_length=200, error_messages={'invalid': _("Ошибка в данных")},
                                     verbose_name=_("Данные адреса доставки"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Итоговая цена"))

    class MovingChoices(models.IntegerChoices):
        place_0 = 0, _("Пункт выдачи")
        place_1 = 1, _("Адрес заказчика")

    move_to = models.PositiveIntegerField(
        choices=MovingChoices.choices, default=MovingChoices.place_0, verbose_name=_("Доставить на")
    )

    class PaymentChoices(models.IntegerChoices):
        payment_0 = 0, _("Ожидает оплаты")
        payment_1 = 1, _("Оплачен")
        payment_2 = 2, _("При вручении, б/н"),
        payment_3 = 3, _("При вручении, нал.д/с")

    payment_conditions = models.PositiveIntegerField(
        choices=PaymentChoices.choices, default=PaymentChoices.payment_0, verbose_name=_("Статус оплаты")
    )

    class StatusChoices(models.IntegerChoices):
        status_0 = 0, _("Заказан")
        status_1 = 1, _("Доставлен"),
        status_2 = 2, _("Отменен")

    status = models.PositiveIntegerField(
        choices=StatusChoices.choices, default=StatusChoices.status_0, verbose_name=_("Статус заказа")
    )

    time_placed = models.DateTimeField(auto_now_add=True, verbose_name=_("Время заказа"))
    time_delivered = models.DateTimeField(blank=True, null=True, verbose_name=_("Время доставки"))

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ('-time_placed',)

    def __str__(self):
        return f"<{self.pk}> {self.phonenumber} --- {self.total_price}"

    def is_ready_to_deliver(self):
        return self.payment_conditions != 0

    def is_delivered(self):
        return self.status == 1

    def reserve(self):
        """Зарезервировать (убрать со склада) выбранное число заказанных позиций,
        не помещая в число продаж (до момента доставки)"""
        products_values = json.loads(self.order_content)
        for product_dict in products_values:
            product = get_object_or_404(Product, id=product_dict['id'])
            quantity = product_dict['quantity']
            product.reserve(quantity)

    def deliver(self):
        """Окончательное списание заказанных позиций с помещением в число продаж (доставка)"""
        products_values = json.loads(self.order_content)
        for product_dict in products_values:
            product = get_object_or_404(Product, id=product_dict['id'])
            quantity = product_dict['quantity']
            product.sale(quantity)
        self.status = Order.StatusChoices.status_1
        self.time_delivered = timezone.now()
        self.save()

    def cancel_reserve(self):
        """Возврат позиций  на склад (в случае отмены заказа или отказа от оплаты)"""
        products_values = json.loads(self.order_content)
        for product_dict in products_values:
            product = get_object_or_404(Product, id=product_dict['id'])
            quantity = product_dict['quantity']
            product.cancel_reserve(quantity)
        self.status = Order.StatusChoices.status_2
        self.time_delivered = timezone.now()
        self.save()


def create_message(instance, prefix='', create=True):
    message_product = f"ID:{instance.pk}"
    if instance.status != 0:
        prefix += f" {instance.get_status_display()}".upper()
    else:
        message_product += f"\n{instance.person_content}\n{instance.address_content}\n{instance.order_content}\n{instance.get_payment_conditions_display()}"
    return f"{prefix}\n{message_product}"


@receiver(post_save, sender=Order)
def send_message_to_bot_post_save_order(sender, instance, **kwargs):
    if settings.TELEGRAM_SEND_NOTIFICATIONS and settings.TELEGRAM_SEND_ORDER_NOTIFICTATION:
        asyncio.run(send_telegram_message(message=create_message(instance, _("Заказ").upper(), create=True)))


@receiver(pre_delete, sender=Order)
def send_message_to_bot(sender, instance, **kwargs):
    if settings.TELEGRAM_SEND_NOTIFICATIONS and settings.TELEGRAM_SEND_ORDER_NOTIFICTATION:
        asyncio.run(send_telegram_message(message=create_message(instance, _("Заказ удален").upper(), create=False)))
