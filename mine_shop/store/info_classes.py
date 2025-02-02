from django.db import models

import asyncio
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from django.utils.translation import gettext as _

from posts.inner_functions import send_telegram_message
from store.models import Product
from users.models import User


class Sale_information(models.Model):
    """
    Модель для хранения технической информации для администрации о продажах и популярности товара
    """
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE, related_name="sale_information")
    sold_count = models.PositiveIntegerField(default=0, blank=False, verbose_name=_("Продажи"))
    viewed_count = models.PositiveIntegerField(default=0, blank=0, verbose_name=_("Просмотры"))
    voted_count = models.PositiveIntegerField(default=0, blank=0, verbose_name=_("Количество оценок"))
    rating = models.DecimalField(default=3, blank=False, max_digits=3, decimal_places=2, verbose_name=_("Рейтинг"))

    class Meta:
        ordering = ('viewed_count', )
        verbose_name = _("Информация о движении изделия")
        verbose_name_plural = _("Информация о движении изделия")

    def sold(self, quantity=1):
        """Логика реализации продажи"""
        self.product.sale(quantity)
        self.sold_count -= quantity
        self.save()

    def view(self):
        """Логика реализации фиксации просмотра страницы"""
        self.viewed_count += 1
        self.save()

    def vote(self, stars):
        """Реализация логики голосования"""
        if self.voted_count == 0:
            self.rating -= 3
        self.voted_count += 1
        self.rating = self.rating + stars
        self.product.vote(self.rating / self.voted_count)
        self.save()

    def del_vote(self, stars):
        self.voted_count -= 1
        self.rating = (self.rating - stars)/self.voted_count if self.voted_count != 0 else 3
        if self.voted_count == 0:
            self.product.vote(0)
        else:
            self.product.vote(self.rating)
        self.save()


class Vote(models.Model):
    """
        Модель для хранения отзыва и оценки пользователя экземпляра продукции
    """
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='votes', verbose_name=_("Продукт"))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='votes', verbose_name=_("Пользователь"))
    name = models.CharField(max_length=75, verbose_name=_("Имя пользователя"))
    stars = models.PositiveSmallIntegerField(choices=Product.RatingChoices, verbose_name=_("Оценка"))
    review = models.TextField(blank=True, null=True, max_length=500, verbose_name=_("Отзыв"))
    time_published = models.DateTimeField(auto_now_add=True, verbose_name=_("Время публикации"))

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ('-time_published',)

    def vote(self):
        s_i, _ = Sale_information.objects.get_or_create(product=self.product)
        s_i.vote(self.stars)

    def del_vote(self):
        s_i, _ = Sale_information.objects.get_or_create(product=self.product)
        s_i.del_vote(self.stars)


def create_message(instance, prefix=''):
    message_product = f"{instance.product.id} - {instance.product.title}" if instance.product else ''
    return f"{prefix}\n{_("Продукт")}: {message_product}\n{_("Пользователь")}: {instance.user}\n*: {instance.stars}\n{instance.review}"


@receiver(pre_save, sender=Vote)
def send_message_to_bot_pre_save_vote(sender, instance, **kwargs):
    asyncio.run(send_telegram_message(message=create_message(instance, _("Отзыв").upper())))


@receiver(pre_delete, sender=Vote)
def send_message_to_bot(sender, instance, **kwargs):
    asyncio.run(send_telegram_message(message=create_message(instance, _("Отзыв удален").upper())))


@receiver(pre_delete, sender=Vote)
def update_rating(sender, instance, **kwargs):
    instance.del_vote()
