from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _

from store.models import Product


class User(AbstractUser):
    username = models.CharField(
            _('имя пользователя'),
            max_length=75,
            help_text=_("Обязательное. Не более 75 символов. Допустимы буквы, цифры и символы @/./+/-/_"),
            validators=[AbstractUser.username_validator],
            error_messages={
                    'unique': _("Пользователь с таким именем уже существует."),
            },
            null=True,
            blank=True,
    )

    email = models.EmailField(_("адрес электронной почты"), unique=True)

    is_active = models.BooleanField(
            _("активный"),
            default=False,
            help_text=_(
                "Отображает, является ли пользователь активным пользователем."
                "Отметьте пользователя неактивнм вместо удаления аккаунта."
            ),

    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserTools(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE, verbose_name=_("Покупатель"))

    max_length_rv = models.SmallIntegerField(default=settings.USER_TOOLS_MAX_LENGTH_RECENTLY_VIEWED, editable=False,
                                                                                    auto_created=True, verbose_name=_("Максимальное число записей в категории 'Недавно просмотренное'"))
    max_length_w = models.SmallIntegerField(default=settings.USER_TOOLS_MAX_LENGTH_WISHLIST, editable=False,
                                                                                    auto_created=True, verbose_name=_("Максимальное число записей в категории 'Избранное'"))
    max_length_c = models.SmallIntegerField(default=settings.USER_TOOLS_MAX_LENGTH_COMPARISON, editable=False,
                                                                                    auto_created=True, verbose_name=_("Максимальное число записей в категории 'Сравнение'"))


    class Meta:
        verbose_name=_("Инструменты авторизованного пользователя")

    @property
    def total_count_rv(self):
        return len(self.rv_items.all())

    @property
    def total_count_w(self):
        return len(self.w_items.all())

    @property
    def total_count_c(self):
        return len(self.c_items.all())

    def add_rv(self, product):
        item, created = self.rv_items.get_or_create(product=product)
        if not created:
            item.save()
        else:
            if self.total_count_rv > self.max_length_rv:
                self.rv_items.last().delete()
                self.save()

    def add_w(self, product):
        item, created = self.w_items.get_or_create(product=product)
        if not created:
            item.save()
        else:
            if self.total_count_w > self.max_length_w:
                self.w_items.last().delete()
                self.save()

    def add_c(self, product):
        item, created = self.c_items.get_or_create(product=product)
        if not created:
            item.save()
        else:
            if self.total_count_c > self.max_length_c:
                self.c_items.last().delete()
                self.save()


class RecentlyViewedItem(models.Model):
    recently_viewed = models.ForeignKey(to=UserTools, on_delete=models.CASCADE, related_name="rv_items")
    added = models.DateTimeField(auto_now=True, verbose_name=_("Просмотрено"))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_("Идентификатор продукта"))

    class Meta:
        verbose_name =  _("Недавно просмотренный товар")
        ordering = ('-added',)


class WishlistItem(models.Model):
    recently_viewed = models.ForeignKey(to=UserTools, on_delete=models.CASCADE, related_name="w_items")
    added = models.DateTimeField(auto_now=True, verbose_name=_("Добавлено"))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_("Идентификатор продукта"))

    class Meta:
        verbose_name =  _("Избранный товар")
        ordering = ('-added',)


class ComparisonItem(models.Model):
    recently_viewed = models.ForeignKey(to=UserTools, on_delete=models.CASCADE, related_name="c_items")
    added = models.DateTimeField(auto_now=True, verbose_name=_("Добавлено"))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_("Идентификатор продукта"))

    class Meta:
        verbose_name =  _("Товар к сравнению")
        ordering = ('-added',)

def superuser():
    print()
    print('Existing superusers:')
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        print(f"    {user}")
    print()


def defaultsuperuser():
    default_superuser = User.objects.get(email='admin@admin.com')
    if not default_superuser:
        default_superuser = User(email='admin@admin.com', is_active=True, is_staff=True, is_superuser=True)
    default_superuser.set_password('12345678')
    default_superuser.save()
    print()
    print('Default superuser is modified:')
    print(f'    {default_superuser},    password: 12345678')
    print()


def createsuperuser():
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email
    from users.inner_functions import PASSWORD_SET

    defaultsuperuser()
    superuser()

    while True:
        email = None
        print()
        while not email:
            print('enter email: ')
            email = input()
            try:
                validate_email(email)
            except ValidationError as e:
                print("bad email, details: ", e)
                email = None

        password = None
        while not password:
            print('enter password: (allowed: letters and digits, not shorter than 8 )')
            password = input()
            if len(password) < 8:
                print(f'bad password, details: length {len(password)} < 8')
                password = None
            elif not set(password).issubset(PASSWORD_SET):
                print("bad , details: allowed letters and digits")
                password = None

        new_superuser = User(email=email, is_active=True, is_staff=True, is_superuser=True)
        new_superuser.set_password(password)
        try:
            new_superuser.save()
            print(f'New superuser {new_superuser} is created and stored in db')
            break
        except Exception as ex:
            print(ex)
