from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django.contrib.auth.models import Group


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False),
        }
