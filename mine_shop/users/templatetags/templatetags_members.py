from django import template

from store.models import Product
from users.inner_functions import get_products_by_tool_items
from users.models import UserTools

register = template.Library()

MEMBER_MESSAGES = {
    '1':  'Пользователь с таким эл.адресом уже зарегистрирован.',
    '2':  'Ссылка активации отправлена на указанную эл.почту.',
    '3': 'Пароль и ссылка активации отправлена на указанную эл.почту.',
    '4': 'Для отправки нового пароля на почту заполните соответствующее поле',
    '5': 'Ищите новый пароль на указанной эл.почте',
    '6': 'Пользователя с таким эл.адресом нет в системе. Введите корректный или пройдите регистрацию',
}

@register.filter
def message_for_key(key):
    return MEMBER_MESSAGES[key]

@register.filter
def usertools(user):
    usertools, _ = UserTools.objects.get_or_create(user=user)
    return usertools

@register.filter
def recently_viewed(usertools):
    rv_items = usertools.rv_items.all()
    return get_products_by_tool_items(rv_items)
