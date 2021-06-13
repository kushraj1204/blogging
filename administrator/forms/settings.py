from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from ..models import Settings
from django.contrib.auth.models import Group


class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'

