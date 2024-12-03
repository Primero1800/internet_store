import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from siteajax.decorators import ajax_dispatch

from cart.inner_functions import get_current_cart
from mine_shop.ajax_maps import ajax_show_basket_header_map, ajax_show_wishcompare_header_map
from users.forms import RegisterForm, UserLoginForm, RestorePasswordForm
from users.inner_functions import generate_password
from users.models import User


@method_decorator(
    ajax_dispatch(
        ajax_show_basket_header_map | ajax_show_wishcompare_header_map,
    ),
    name='dispatch'
)
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'users/registration.html'

    def __init__(self):
        super().__init__()
        self.message_for_member = None
        self.placeholder_email = None

    def form_valid(self, form):
        user, created = User.objects.get_or_create(email=form.cleaned_data["email"])
        new_password = None

        self.placeholder_email = user.email
        self.message_for_member = '1'

        if created:
            new_password = generate_password()
            user.set_password(new_password)
            user.save(update_fields=['password', ])

        if new_password or not user.is_active:
            self.message_for_member = '2'
            token = uuid.uuid4().hex
            redis_key = settings.MINE_SHOP_USER_CONFIRMATION_KEY.format(token=token)

            cache.set(redis_key, {"user_id": user.id}, timeout=settings.MINE_SHOP_USER_CONFIRMATION_TIMEOUT)

            confirm_link = self.request.build_absolute_uri(
                reverse_lazy(
                    "users:registration_confirm", kwargs={'token': token}
                )
            )

            message = _(f"Для завершения регистрации и активации аккаунта \n"
                        f"пройдите по ссылке {confirm_link} \n")

            if new_password:
                message += _(f"Ваш новый пароль {new_password} \n")
                self.message_for_member = '3'

            send_mail(
                    subject=_(f"{settings.STORE_TITLE} Пожалуйста, подтвердите регистрацию"),
                    message=message,
                    from_email="primero@inbox.ru",
                    recipient_list=[user.email, ]
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:login", kwargs={"message": self.message_for_member, "email": self.placeholder_email})



def registration_confirm(request, token):
    redis_key = settings.MINE_SHOP_USER_CONFIRMATION_KEY.format(token=token)
    user_info = cache.get(redis_key) or {}

    user_id = user_info.get('user_id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save(update_fields=['is_active', ])
        return redirect(to=reverse_lazy("users:login", kwargs={"message": '3', "email": user.email}))
    else:
        return redirect(to=reverse_lazy("users:registration"))


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def login(request, message=None, email=None, next=None):
    context = {}
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            anonimous_cart = get_current_cart(request)
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                cart = get_current_cart(request)
                cart += anonimous_cart
                next = request.POST['next'] if 'next' in request.POST else None
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('store:index'))
            context = {'auth_error': _("Проверьте имя и пароль")}
    else:
        context['next'] = request.GET['next'] if 'next' in request.GET else None
        form = UserLoginForm()
        context['member_message'] = message
        context['email_placeholder'] = email
    context['form'] = form
    return render(request, 'users/login.html', context)

@login_required(login_url=reverse_lazy("users:login"), redirect_field_name='next')
def logout(request):
    auth.logout(request)
    return redirect(to=reverse_lazy('store:index'))


@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def restore_password(request):
    context, kwargs, user = {}, {}, None
    if request.method == 'POST':
        form = RestorePasswordForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
            except:
                context['member_message'] = '6'

            if user:
                new_password = generate_password()
                user.set_password(new_password)
                user.save(update_fields=['password', ])
                message = _(f"Ваш новый пароль: {new_password}")

                send_mail(
                    subject=_(f"{settings.STORE_TITLE} Восстановление доступа"),
                    message=message,
                    from_email="primero@inbox.ru",
                    recipient_list=[user.email, ]
                )

                return redirect(to=reverse_lazy("users:login", kwargs={"message": '5', "email": user.email}))

    else:
        form = RestorePasswordForm()
    context['form'] = form
    return render(request, "users/restore_password.html", context)


@login_required(login_url=reverse_lazy("users:login"), redirect_field_name='next')
@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def wishlist(request):
    context = {}
    return render(request, 'users/wishlist.html', context)


@login_required(login_url=reverse_lazy("users:login"), redirect_field_name='next')
@ajax_dispatch(ajax_show_basket_header_map | ajax_show_wishcompare_header_map)
def comparison(request):
    context = {}
    return render(request, 'users/comparison.html', context)