from django import forms

from django.utils.translation import gettext as _


class VoteForm(forms.Form):
    name = forms.CharField(
        required=True, max_length=75, min_length=2, widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={"required": _("Обязательное условие"), },
        label=_("Отображаемое имя")
    )
    email = forms.EmailField(
        required=False, min_length=3, max_length=70,
        widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={
            'max_length': _("Не более 70 символов"),
            'min_length': _("Не менее 3 символов")
        },
        label=_("Адрес эл.почты")
    )
    stars = forms.IntegerField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control;'}),
        label=_("Оценка")
    )
    review = forms.CharField(
        required=False, max_length=500, widget=forms.TextInput(attrs={'class': 'form-control;'}),
        error_messages={'max_length': _("Не более 500 символов")}, label = _("Отзыв")
    )
