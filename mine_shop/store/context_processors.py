import django.conf


def add_currency_to_context(request):
    return {'currency': django.conf.settings.CURRENCY}


def add_store_title_to_context(request):
    return {'store_title': django.conf.settings.STORE_TITLE}
