from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    confirmation = forms.BooleanField(
        widget=forms.RadioSelect(attrs={"class": "form-control;"}),
        error_messages={"required": _("Обязательное условие"), }, label=_("Согласие")
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': "form-control;"}),
        error_messages={"required": _("Не может быть пустым")}, label=_("Адрес эл.почты")
    )

    def clean_confirmation(self):
        if self.cleaned_data['confirmation'] is not True:
            raise ValidationError(_("Необходимо согласие на обработку персональных данных"))


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': "form-control;"}),
        error_messages={"required": _("Не может быть пустым")}, label=_("Адрес эл.почты")
    )
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'class': "form-control;"}),
        error_messages={"required": _("Не может быть пустым")}, label=_("Пароль")
    )


class RestorePasswordForm(forms.Form):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': "form-control;"}),
        error_messages={"required": _("Не может быть пустым")}, label=_("Адрес эл.почты")
    )
