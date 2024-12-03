from django import template
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def from_key(key):
    if key in DICTIONARY:
        return DICTIONARY[key]
    return DICTIONARY['unknown']

DICTIONARY ={
    'unknown': _("UNKNOWN"),

    'ID': _("ID"),
    'anonimous': _("Аноним"),
    'price': _("Цена"),
    'compare': _("Сравнить"),
    'exit': _("Выход"),
    'enter': _("Вход"),
    'to_enter': _("Войти"),
    'email': _("Адрес электронной почты"),
    'password': _("Пароль"),
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
    'find': _("Найти"),

    ################### STORE_CONSTANTS

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

    # 500.html
    '500_exception': _("Внутренняя ошибка сервера. Обновите страницу через минуту"),
    '500_title': _("Ошибка 500"),

    # 403.html
    '403_title': _("Ошибка 403"),
    '403_exception': _("Страница недоступна неавторизованному пользователю"),
    '403_link': _("На страницу авторизации"),

    # 400.html
    '400_exception': _("Некорректный запрос"),
    '400_title': _("Ошибка 400"),


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
    'df_find_us_in_sn': _("Ищите нас в социальных сетях"),
    'df_find_it_fast': _("Быстрый переход"),


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

    #### ORDERS CONSTANTS

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
    'A_all': _("Итого"),
    'A_delivered': _("Доставлено"),
    'A_awaits': _("Ожидает"),
    'A_cancelled': _("Отменено"),
    'A_count': _("Количество"),
    'A_last_delivery': _("Последняя доставка"),
    'A_long_await': _("Длительное ожидание"),
    'status_0': _("заказан"),
    'status_1': _("доставлен"),
    'status_2': _("отменен"),
    'payment_conditions_0': _("предоплата"),
    'payment_conditions_1': _("оплачено"),
    'payment_conditions_2': _("карта"),
    'payment_conditions_3': _("наличн."),

    # ajax_div_total_field
    'adtf_total_pay': _("Итого к оплате"),

    ### USERS CONSTANTS

    # comparison
    'uc_title': _("Сравнение тваров"),

    # login
    'ul_title' :_("Аутентификация"),
    'ul_enter_account': _("Войти в существующий аккаунт"),
    'ul_no_account_register': _("Нет аккаунта? Зарегистрируйтесь"),
    'ul_facebook_signin': _("!!!Sign in with facebook!!!"),
    'ul_twitter_signin': _("!!!Sign in with twitter!!!"),
    'ul_forget_password_get_new': _("Забыли пароль? Отправить новый на указанную почту"),

    # registration
    'ur_create_new_account': _("Создать новый аккаунт"),
    'ur_have_account_enter': _("Уже есть аккаунт? Выполните вход"),
    'ur_agree_to_personalize': _("Согласен на обработку персональных данных"),
    'ur_register': _("Зарегистрироваться"),
    'ur_register_now_and_get': _("Зарегистрируйтесь сегодня и вы получите"),
    'ur_rule1': _("Хранение корзины заказов на сервере с возможностью доступа с различных устройств"),
    'ur_rule2': _("Ускорение оформления заказа с сохранением в истории"),
    'ur_rule3': _("Разделы сравнения товаров и добавления в избранное"),
    'ur_rule4': _("Возможность оценивать товары и участвовать в обсуждениях"),
    'ur_rule5': _("Возможность быстрого доступа к ранее просмотренным позициям"),
    'ur_rule6': _("Возможность оставлять комментарии на форуме сайта"),

    # restore_password
    'urp_title': _("Восстановление пароля"),
    'urp_change_password': _("Изменить пароль"),
    'urp_remember_password_enter': _("Вспомнили пароль? Войти"),
    'urp_no_account_register': _("Нет аккаунта? Зарегистрируйтесь"),
    'urp_send_password': _("Выслать новый пароль"),

    # ajax_div_comparison_content
    'rp_adcc_compare_positions': _("Сравнение позиций"),
    'rp_adcc_comparison_empty': _("Список для сравнения пуст"),


    ##### POSTS CONSTANTS

    # blog
    'p_forum_title': _("Форум"),
    'p_follow': _("Перейти"),
    'p_authorized_only': _("Участие в дискуссии могут принимать только авторизованные пользователи."),
    'p_no_posts': _("Сообщения отсутствуют"),
    'p_posts': _("Сообщения"),
    'p_about_forum': _("О форуме"),
    'p_blog_rules': _("Сообщения могут оставлять только авторизованные пользователи. Сообщения могут быть как на общие темы, так о какой-либо единице продукции. Пользователь может указать ее в выпадающем списке в виде ссылки на страницу продукта или используя наименование. При общении будьте вежливы друг с другом и корректны в своих сообщениях. Помните, что их читают тоже люди :)"),
    'p_add_post': _("Оставить сообщение"),
    'p_public': _("Опубликовать"),
    'p_enter_link_or_name': _("Введите ссылку или имя товара"),
    'p_not_found': _("Товар не найден"),
    'p_not_chosen': _("Товар не выбран"),
    'p_about_product': _("О продукте"),
    'p_recent_in_posts': _("Последнее в публикациях"),

    # information
    'p_info_title': _("О сайте"),
    'p_info_link': _("Информация / контакты"),
    'p_authors': _("Создатели"),
    'p_author': _("Алексей Кулеш"),
    'p_author_contacts': _("Контакты"),
    'p_used_frameworks': _("Использовались технологии"),
    'p_info_inner_header': _("Структура проекта"),

    'p_info_store': _("Реализует основу интернет-магазина с экземплярами товаров в продаже, с системой поиска, фильтрации и различных способов "
                      "отображения выбранных позиций. Дополнительно представлены брэнды, категории товаров, "
                      "необязательная дополнительная информация о каждом экземпляре, информация о движении (продажа, просмотры и т.д), отдельный класс-модель "
                      "изображений для продукции и отзывы, оставляемые авторизованными пользователями."),
    'p_info_cart': _("Реализует корзину покупателя. Реализация для анонима и авторизованного пользователя различаются. Поведение корзины анонима из сессии "
                     "при авторизации пользователя реализуется двумя различными способами, выбор между которыми осуществляется в файле настроек проекта."),
    'p_info_users': _("Аутентификация пользователей осуществляется по адресу почтового ящика, куда высылается пароль при регистрации на сайте. "
                      "В случае утери пароля есть механизм восстановления. После регистрации пользователю необходимо активировать свой аккаунт. "
                      "Зарегистрированный пользователь получает возможность участвовать в дискуссиях, оценивать продукцию, добавлять позиции в избранное "
                      "и список сравнения, просматривать свою историю заказов. Кроме того сохраняются персональны данные, что упрощает саму процедуру заказа."),
    'p_info_orders': _("Реализует систему заказов. Зарегистрированные пользователи сохраняют свои данные для автоматического заполнения при последующих обращениях. "
                       "Кроме того, имеется возможность просматривать историю заказов, а для адмнинистрации сайта - удобные инструменты для обработки заказов. "
                       "Данные о заказаных позициях и пользователях хранятся в БД в сериализованном виде."),
    'p_info_posts': _("Реализация простого форума с возможностью для зарегистрированных пользователей оставлять комментарии как на общую тему, "
                      "так и касательно определенного экземпляра продукции (благодаря системе поиска и выбора)"),
    'p_info_image_index': _("Фрагмент стартовой страницы"),
    'p_info_image_product': _("Фрагмент страницы экземпляра"),
    'p_info_image_rubric': _("Фрагмент страницы категории"),
    'p_info_image_forum': _("Фрагмент страницы форума"),
    'p_info_image_admin_orders': _("Фрагмент страницы обработки заказов"),
    'p_info_image_orders_history': _("Фрагмент страницы истории заказов"),
    'p_info_image_cart_dropdown': _("Корзина в меню"),
    'p_info_image_cart_inner': _("Корзина изнутри"),
    'p_info_image_wishlist': _("Избранное"),
    'p_info_image_comparison': _("Сравнение позиций"),
    'p_info_image_filters': _("Фильтры"),
    'p_info_image_orders': _("Страница заказа"),


}