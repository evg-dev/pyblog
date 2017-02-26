from django import forms
from django.forms import ModelForm, TextInput, EmailInput, Textarea,  widgets as w
from django.utils.translation import ugettext_lazy as _
from blog.models import Comment
from captcha.fields import CaptchaField


class Contact(forms.Form):
    title = forms.CharField(label=_('Theme:'), max_length=100)
    name = forms.CharField(label=_('Name:'), max_length=100)
    mail = forms.EmailField(label=_('Email:'), max_length=100)
    text = forms.CharField(label=_('Message:'), widget=forms.Textarea)
    # captcha = CaptchaField(label=_('Captcha:'))


class CommentForm(ModelForm):
    required_css_class = 'required_field'
    # captcha = CaptchaField(label=_('Captcha:'))

    class Meta:
        model = Comment
        fields = ['user_name', 'user_email', 'user_url', 'content']
        labels = {
            'user_url': _('Website')
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['user_email'].required = True
