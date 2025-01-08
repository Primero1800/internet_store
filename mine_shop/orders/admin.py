from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Order


def deliver(modeladmin, request, queryset):
    for order in queryset:
        if order.status == 0:
            order.deliver()
    modeladmin.message_user(request, _("Заказы доставлены"))


deliver.short_description = _("Доставить")


def cancel_reserve(modeladmin, request, queryset):
    for order in queryset:
        if order.status == 0:
            order.cancel_reserve()
    modeladmin.message_user(request, _("Заказы отменены"))


cancel_reserve.short_description = _("Отменить заказ")


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'time_placed', 'time_delivered', 'payment_conditions', 'total_price',
        'phonenumber', 'user', 'address_content', 'person_content', 'order_content'
    )
    list_display_links = ('id', 'status', 'time_placed', 'time_delivered',)
    search_fields = ('id', 'status', 'total_price', 'phonenumber', 'address_content', 'person_content', 'order_content')
    list_filter = ('status', 'payment_conditions', 'phonenumber', 'user')
    date_hierarchy = 'time_placed'

    list_per_page = 30
    actions_on_top = False
    actions_on_bottom = True

    readonly_fields = ('time_placed', 'id', 'time_delivered', )

    fieldsets = (
        (None, {
            'fields': (('id', 'status'), ('phonenumber', 'user'), ('person_content', 'address_content')),
            'classes': ('wide',)
        }),
        (_("Содержимое заказа"), {
            'fields': ('order_content',),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('total_price', 'payment_conditions', 'move_to',),),
            'classes': ('wide',)
        }),
        (None, {
            'fields': ('time_placed', 'time_delivered',),
            'classes': ('wide',)
        }),
    )

    radio_fields = {
        'status': admin.VERTICAL,
        'payment_conditions': admin.VERTICAL,
        'move_to': admin.VERTICAL,
    }

    actions = (deliver, cancel_reserve,)

    def view_on_site(self, pk):
        return reverse('orders:admin_orders')


admin.site.register(Order, OrderAdmin)
