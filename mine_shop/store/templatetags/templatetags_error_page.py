from django import template
from django.utils.translation import gettext as _

register = template.Library()

ERROR_PAGE_MESSAGES = {
    0:  _("Страница не найдена"),
    1: _("Для просмотра истории заказов пройдите по ссылке: "),
}


ERROR_PAGE_LINKS = {
    1: "orders:history",
}


@register.filter
def message_for_key(key):
    return ERROR_PAGE_MESSAGES[key]


@register.filter
def link_for_key(key):
    return ERROR_PAGE_LINKS[key]