from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinLengthValidator

import asyncio
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from posts.inner_functions import send_telegram_message
from store.models import Product
from users.models import User


class Post(models.Model):
    """
        Модель для хранения сообщения на форуме
    """
    product = models.ForeignKey(
        to=Product, blank=True, null=True, on_delete=models.CASCADE,
        related_name='posts', verbose_name=_("Продукт"),
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='posts', verbose_name=_("Пользователь")
    )
    name = models.CharField(max_length=75, verbose_name=_("Имя пользователя"))
    review = models.TextField(max_length=500, verbose_name=_("Отзыв"), validators=[
                                                            MinLengthValidator(1, _("Не менее одного символа"))])
    time_published = models.DateTimeField(auto_now_add=True, verbose_name=_("Время публикации"))

    class Meta:
        verbose_name = _("Сообщение")
        verbose_name_plural = _("Сообщения")
        ordering = ('-time_published',)


def create_message(instance, prefix=''):
    message_product = f"{instance.product.id} - {instance.product.title}" if instance.product else ''
    return f"{prefix}\n{_("Имя")}: {instance.name}\n{_("Продукт")}: {message_product}\n{instance.review}"


@receiver(pre_save, sender=Post)
def send_message_to_bot(sender, instance, **kwargs):
    asyncio.run(send_telegram_message(message=create_message(instance, _('Сообщение').upper())))


@receiver(pre_delete, sender=Post)
def send_message_to_bot(sender, instance, **kwargs):
    asyncio.run(send_telegram_message(message=create_message(instance, _('Сообщение удалено').upper())))
