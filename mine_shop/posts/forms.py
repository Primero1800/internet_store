from django import forms

from django.utils.translation import gettext as _

from store.forms import VoteForm


class PostForm(VoteForm):
    stars = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control;'}),
                           label=_('Оценка'))
    review = forms.CharField(required=True, max_length=500, widget=forms.TextInput(attrs={'class': 'form-control;'}),
                            error_messages={
                                'required': _("Обязательное условие"),
                                'max_length': _("Не более 500 символов")},
                            label = _('Сообщение'))
