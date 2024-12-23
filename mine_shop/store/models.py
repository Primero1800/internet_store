from decimal import Decimal
from django.utils.translation import gettext as _

from django.db import models

import store


class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_("Описание"))
    image = models.ImageField(verbose_name=_("Логотип"), blank=True, upload_to='brands/')

    class Meta:
        verbose_name = _("Производитель")
        verbose_name_plural = _("Производители")
        ordering = ('title', )

    def __str__(self):
        return f"<Brand> {self.title}"

    def get_products_count(self):
        return len(self.items.all())


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Наименование"), unique=True)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    brand = models.ForeignKey(Brand, related_name="items", verbose_name=_("Производитель"), on_delete=models.CASCADE)
    rubrics = models.ManyToManyField('Rubric', verbose_name=_("Рубрики"), related_name='products')
    start_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Начальная цена"))

    class DiscontChoices(models.IntegerChoices):
        D0 = 0, _("без скидки")
        D5 = 5, _("5% скидка")
        D10 = 10, _("10% скидка")
        D15 = 15, _("15% скидка")
        D20 = 20, _("20% скидка")
        D25 = 25, _("25% скидка")
        D30 = 30, _("30% скидка")
        D35 = 35, _("35% скидка")
        D40 = 40, _("40% скидка")
        D45 = 45, _("45% скидка")
        D50 = 50, _("50% скидка")
        D55 = 55, _("55% скидка")
        D60 = 60, _("60% скидка")
        D65 = 65, _("65% скидка")
        D70 = 70, _("70% скидка")

    discont = models.PositiveIntegerField(
        choices=DiscontChoices.choices, default=DiscontChoices.D0,
        verbose_name=_("Скидка")
    )

    class RatingChoices(models.IntegerChoices):
        R0 = 0, _("Нет голосов")
        R1 = 1, _("Ужасно")
        R2 = 2, _("Плохо")
        R3 = 3, _("Средне")
        R4 = 4, _("Хорошо")
        R5 = 5, _("Отлично")

    rating = models.PositiveIntegerField(
        choices=RatingChoices.choices, default=RatingChoices.R0,
        verbose_name=_("Рейтинг изделия")
    )

    AVAILABLE_CHOICES = (
        ('0', _("в продаже")),
        ('1', _("нет в наличии")),
    )
    available = models.CharField(choices=AVAILABLE_CHOICES, default=AVAILABLE_CHOICES[0], max_length=50)
    published = models.DateTimeField(auto_now_add=True, verbose_name=_("Опубликовано"))
    quantity = models.PositiveIntegerField(default=0, verbose_name=_("Количество"))

    def __str__(self):
        return f"{self.slug}"

    def is_available(self):
        """ TRUE / FALSE      Возвращает есть ли товар в продаже (на остатках больше 0) """
        if self.quantity == 0:
            self.available = '1'
            return False
        return self.quantity > 0

    def reserve(self, quantity=1):
        """Процедура списания товара и установки при необходимости недоступности """
        self.quantity -= quantity
        if self.quantity == 0:
            self.available = Product.AVAILABLE_CHOICES[1][0]
        self.save()

    def cancel_reserve(self, quantity=1):
        """Процедура отмены списания товара и восстановления при необходимости доступности """
        self.quantity += quantity
        self.available = Product.AVAILABLE_CHOICES[0][0]
        self.save()

    def  sale(self, quantity=1):
        """Процедура регистрации товара в продажах """
        sale_information, created = store.info_classes.Sale_information.objects.get_or_create(product=self)
        sale_information.sold_count += quantity
        sale_information.save()

    def vote(self, rating):
        self.rating = rating // 1
        delta = rating % 1
        if delta >= 0.5:
            self.rating += 1
        self.save()

    @property
    def price(self):
        """ Свойство, динамически вычисляющее текущую цену на основе стартовой и скидки"""
        return round(self.start_price * Decimal(1-self.discont/100), 2)

    price.fget.short_description = _("Цена")

    def is_on_sale(self):
        """ TRUE/FALSE      Возвращает, есть ли у товара скидка"""
        return self.discont != Product.DiscontChoices.D0

    is_on_sale.short_description = _("На скидке")

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукция")
        ordering = ('-pk', )


class Image(models.Model):
    """ images 433 X 325 for Product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def get_image_path(self, filename):
        return f"images/{self.product.pk}/{filename}"
    image = models.ImageField(upload_to=get_image_path, verbose_name=_("Изображение"))

    class Meta:
        verbose_name = _("Изображение")
        verbose_name_plural = _("Изображения")


class Additional_information(models.Model):
    """ Дополнительная информация для Product"""
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Вес в упаковке"), blank=True, default=2.0
    )
    dimensions = models.CharField(max_length=30, default=_("Неизвестно"), verbose_name=_("Размер упаковки"))
    size = models.CharField(max_length=50, verbose_name=_("Доп.указания"), default=_("Неизвестно"))
    guarantee = models.CharField(max_length=50, verbose_name=_("Гарантия"), default=_("Без гарантийных обязательств"))
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Дополнительная информация")

    def verbose_name(self, field):
        return Additional_information.meta.get_field(field).verbose_name


class Rubric(models.Model):
    """
    Класс для фильтрации основного класса Product по категориям.
    Отношение many2many, ведомый .
    Основное изображение - 899X277
    """
    title = models.CharField(max_length=50, verbose_name=_("Наименование"), unique=True)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_("Описание"))
    image = models.ImageField(upload_to='rubrics/', blank=True, verbose_name=_("Изображение"))

    def __str__(self):
        return f'<Rubric> {self.title}'

    class Meta:
        verbose_name = _("Рубрика")
        verbose_name_plural = _("Рубрики")
        ordering = ('id', )
