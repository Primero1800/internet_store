from django import forms
from phonenumber_field.formfields import SplitPhoneNumberField

from django.utils.translation import gettext as _


class PhoneNumberField(SplitPhoneNumberField):
    def invalid_error_message(self):
        return _("Неверный номер для выбранного региона.")


class OrderInformationForm(forms.Form):
    name = forms.CharField(
        required=True, max_length=50, min_length=2,
        widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={"required": _("Обязательное условие"), }, label=_("Имя")
    )
    surname = forms.CharField(
        required=False, initial='', max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={'max_length': _("Не более 50 символов")}, label=_("Фамилия")
    )
    company_name = forms.CharField(
        required=False, initial='', max_length=100, min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={'max_length': _("Не более 50 символов"),
                                           'min_length': _("Не менее 3 символов")},
        label=_("Компания"), help_text=_("*для юридических лиц"))

    address = forms.CharField(required=True, min_length=5, widget=forms.TextInput(attrs={'class': 'form-control;'}),
                                   error_messages={'required': _("Обязательно условие"),
                                                                     'min_length': _("Не менее 5 символов")},
                           label=_("Адрес доставки"))
    city = forms.CharField(required=True, min_length=2, widget=forms.TextInput(attrs={'class': 'form-control;'}),
                                   error_messages={'required': _("Обязательно условие"),
                                                                    'min_length': _("Не менее 2 символов")},
                           label=_("Населенный пункт"))
    postcode = forms.IntegerField(
        required=False, initial=0, min_value=0, max_value=999999999999,
        widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={'required': _("Обязательно условие"),
                                           'invalid': _("Неверное значение"),
                                           'max_value': _("Не более 12 символов"),
                                           'min_value': _("Не менее 2 символов")},
        label=_("Почтовый код"))
    email = forms.EmailField(
        required=False, min_length=3, max_length=70,
        widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={'max_length': _("Не более 70 символов"),
                                          'min_length': _("Не менее 3 символов")},
        label=_("Адрес эл.почты"))

    phonenumber = PhoneNumberField(
                                   error_messages={'required': _("Обязательное условие"),
                                   },
                           label=[_("Код страны"), _("Номер телефона")])
