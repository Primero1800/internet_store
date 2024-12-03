import asyncio

import telegram
from telegram.ext import Updater

from django.conf import settings

from store.models import Product


def correct_by_word_length(text, l):
    words = text.strip().split()
    result = []
    for word in words:
        if len(word) > l:
            i = l
            while i < len(word):
                word=word[:i]+'\n'+word[i:]
                i += l + 1
        result.append(word)
    return ' '.join(result)


def get_product_by_link(link):
    slugs = link.split('/')[-2:]
    for slug in [slug for slug in slugs if slug]:
        product = Product.objects.filter(slug=slug).first()
        if product:
            return product
    return None

def get_product_by_title(title):
    product = Product.objects.filter(title=title).first()
    return product if product else None


def get_verbose_name(instance, field):
    return instance._meta.get_field(field).verbose_name


async def send_telegram_message(message):
    """
    Асинхронная функция для отправки сообщения в ТГ.
    """
    try:
        bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        await bot.send_message(chat_id=chat_id, text=message)
        return 200
    except Exception as ex:
        await asyncio.sleep(0)
        return ex