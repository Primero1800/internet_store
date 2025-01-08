from django.urls import path

from orders.views import orders, orders_history, admin_orders, proceed_order, orders_message

app_name = 'orders'


urlpatterns = [
    path('', orders, name="index"),
    path('history/', orders_history, name='history'),
    path('history/<success>/', orders_history, name='history'),
    path('admin_orders/', admin_orders, name='admin_orders'),

    path('cancel_order/', proceed_order, name='cancel_order'),
    path('deliver_order/', proceed_order, name='deliver_order'),

    path('orders_message/', orders_message, name='orders_message'),
]
