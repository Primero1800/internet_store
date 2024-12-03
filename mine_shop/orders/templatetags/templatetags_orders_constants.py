from django import template
from django.utils.translation import gettext as _

register = template.Library()

DICTIONARY = {
    'button_cancel_order': _("Отмена заказа"),
    'orders_title': _("Заказы"),
    'orders_pcs': _("шт"),
    'do_order': _("Заказать"),
    'user': _("Пользователь"),

    # ORDERS
    'O_user_data_for_delivery': _("Пользовательские данные для доставки"),
    'O_required_fields': _("Отметка обязательных к заполнению полей"),
    'O_not_finished': _("Еще не закончили"),
    'O_follow_link_to_continue': _("Перейдите по ссылке для продолжения покупок"),
    'O_your_order': _("Ваш заказ"),
    'O_correct_quantity': _("в заказе уточнено наличие и количество продукции"),
    'O_edit_order': _("Редактировать"),
    'O_delivery': _("Доставка"),
    'O_order_price': _("Стоимость заказа"),
    'O_autodelivery': _("Самовывоз"),
    'O_direct_banking': _("Предварительная оплата на сайте"),
    'O_direct_banking_text': _("Оплата на сайте посредством предварительного прямого банковского перевода или посредством системы ЕРИП"),
    'O_pay_card': _("Оплата картой при получении"),
    'O_pay_card_text': _("Оплата при получении товара от курьера или в точке самовывоза посредством банковской карты"),
    'O_pay_cash': _("Оплата наличными при получении"),
    'O_pay_cash_text': _("Оплата при получении товара от курьера или в точке самовывоза наличными денежными средствами"),
    'O_empty_cart_no_order': _("Корзина пуста. Заказ невозможен"),
    'O_follow_link_to_continue': _("перейдите по ссылке для совершения покупок"),
    'O_view_orders_history': _("Смотреть историю заказов"),


    # ORDERS_HISTORY
    'unknown': _("UNKNOWN"),
    'O_H_title': _("Заказы. Информация"),
    'O_H_order_created': _("Заказ принят в обработку"),
    'O_H_user_orders_history': _("История заказов пользователя"),

    'O_H_payment_conditions_0': _("Ожидает оплаты"),
    'O_H_payment_conditions_1': _("Оплачен"),
    'O_H_payment_conditions_2': _("Оплата при вручении, б/н"),
    'O_H_payment_conditions_3': _("Оплата при вручении, нал.д/с"),

    'not_allowed_for_anonimous_user': _("Инструмент недоступен для неавторизованного пользователя."),
    'authenticate': _("Пройдите по ссылке для авторизации"),

    # ORDERS_MESSAGE
    'O_M_title': _("Отмена заказа"),
    'O_M_0': _("Заказ отменен"),
    'to_home_page': _("На домашнюю страницу"),

    # ADMIN_ORDERS
    'admin_orders_title': _("Админ. Заказы"),
    'A_button_cancel_order': _("отменить"),
    'A_button_deliver_order': _("доставить"),
    'status_0': _("заказан"),
    'status_1': _("доставлен"),
    'status_2': _("отменен"),
    'payment_conditions_0': _("предоплата"),
    'payment_conditions_1': _("оплачено"),
    'payment_conditions_2': _("карта"),
    'payment_conditions_3': _("наличн."),

    # ajax_div_total_field
    'adtf_total_pay': _("Итого к оплате"),

}

@register.filter
def from_key(key):
    if key in DICTIONARY:
        return DICTIONARY[key]
    return DICTIONARY['unknown']