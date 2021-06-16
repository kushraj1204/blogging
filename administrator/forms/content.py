from django.forms import ModelForm

from blogs.models import Content


class ContentForm(ModelForm):
    class Meta:
        model = Content
        exclude = ['alias']
