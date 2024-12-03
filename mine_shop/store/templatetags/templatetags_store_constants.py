from django import template
from django.utils.translation import gettext as _

register = template.Library()

DICTIONARY = {
    'unknown': _("UNKNOWN"),

    'anonimous': _("Аноним"),
    'exit': _("Выход"),
    'enter': _("Вход"),
    'registration': _("Регистрация"),
    'new_arrival': _("Новинка"),
    'new_arrivals': _("Новинки"),
    'sale': _("Скидка"),
    'bestseller': _("Бестселлер"),
    'bestsellers': _("Бестселлеры"),
    'most_viewed': _("Лидеры просмотров"),
    'top_sales': _("Лидеры продаж"),
    'top_rated': _("Лидеры рейтинга"),
    'not_available': _("Нет в наличии"),
    'basket': _("Корзина"),
    'to_basket': _("В корзину"),
    'add': _("Добавить"),
    'add_to_cart': _("Добавить в корзину"),
    'added': _("Добавлено"),
    'brands': _("Брэнды"),
    'filters': _("Фильтры"),
    'all_products': _("Все товары"),
    'all_products_from_rubric': _("Все товары из категории"),
    'information': _("Информация"),
    'cart': _("Корзина"),
    'cart_of_buyer': _("Корзина покупателя"),
    'orders_history': _("История заказов"),
    'orders': _("Заказы"),
    'to_order': _("К заказу"),
    'wishlist': _("Избранное"),
    'comparison': _("Список сравнения"),
    'grid': _("решетка"),
    'list': _("список"),
    'administration': _("Администрация"),
    'rubrics': _("Категории"),
    'head_rubrics': _("Разделы"),
    'follow_to_rubric': _("Перейти к разделу"),
    'all_rubrics': _("Все категории"),
    'products_on_sale': _("Акционные товары"),
    'all_sales': _("Все скидки"),
    'on_sale': _("На скидке"),
    'sales_more_': _("Скидки более"),
    'tools': _("Инструменты"),
    'product_id': _("ID продукта"),
    'popular': _("Популярное"),
    'recently_viewed': _("Недавно просмотренные"),
    'home_page': _("Стартовая страница"),
    'forum': _("Форум"),
    'admin_tools': _("Инструменты администрации"),
    'orders_tools': _('Работа с заказами'),
    'all_over': _("Итого"),
    'delivery': _("Доставка"),

    # ajax_div_grid_tab
    'adgt_shown_': _("Показано"),
    'adgt_results_': _("результатов"),

    # ajax_div_list_tab
    'adlt_shown_': _("Показано"),
    'adlt_results_': _("результатов"),


    # ajax_div_category_grid
    'adcg_show_more': _("показать еще"),

    # ajax_div_comments
    'c_admin': _("админ"),
    'c_current_food_no_comments': _("У выбранного товара еще нет отзывов и оценок"),
    'c_add_review': _("Добавить отзыв"),
    'c_add': _("Добавить"),
    'c_already_voted': _("Вы уже оценивали выбранный товар"),
    'c_only_authorized': _("Оставлять отзывы могут только авторизованные пользователи"),
    'c_your_vote': _("Ваш отзыв"),

    # ajax_div_grid_tab

    # category-grid
    'cg_filters': _("Фильтры"),
    'cg_show_all': _("Показать все"),
    'cg_new_arrivals': _("Новинки"),
    'cg_on_sale': _("На скидке"),
    'cg_searching_for_key_': _("Поиск по ключу"),
    'cg_in_rubric_': _("в разделе"),
    'cg_following_link': _("Переход по ссылке"),
    'cg_found_products': _("Найдено товаров"),
    'cg_by_default': _("По умолчанию"),
    'cg_by_arriving': _("По поступлению"),
    'cg_by_price': _("По цене"),
    'cg_by_rating': _("По рейтингу"),
    'cg_on_page_': _("на странице"),

    # 404.html
    '404_title': _("Ошибка 404"),
    'to_home_page': _("На домашнюю страницу"),

    # INDEX
    'i_on_chosen_product_': _("на выбранный товар"),
    'i_buy_now': _("Купить прямо сейчас"),
    'i_most_viewed': _("Лидеры просмотров"),
    'i_new_arrivals': _("Новинки"),
    'i_top_sales': _("Лидеры продаж"),
    'i_no_sales': _("Продажи отсутствуют"),

    # SINGLE_PRODUCT
    'sp_availability': _("Доступность"),
    'sp_description': _("Описание"),
    'sp_additional_information': _("Дополнительная информация"),
    'sp_reviews_and_votes': _("Отзывы и оценки"),
    'sp_product_moving': _("Движение товара"),

    # div_featured_products_vertical

    # div_footer

    # div_header
    'dh_all_rubrics': _("Все категории"),
    'dh_find_product': _("Поиск товара"),

    # div_horizontal_navigation

    # div_recently_viewed

    # div_top_brands
    'dtb_top_brands': _("Топ брэнды"),

    # CART
    'cart_title': _("Корзина покупателя"),
    'cart_pcs': _("шт"),
    'cart_is_empty': _("Корзина пуста"),
    'cart_without_delivery': _("Без учета доставки"),
    'cart_order': _("Оформить заказ"),
    'cart_continue_shopping': _("Продолжить покупки"),

}

@register.filter
def from_key(key):
    if key in DICTIONARY:
        return DICTIONARY[key]
    return DICTIONARY['unknown']