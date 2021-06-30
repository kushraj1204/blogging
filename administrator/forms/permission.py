from django.forms import ModelForm
from django.contrib.auth.models import Permission
from blogs.models import Category


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'
