from django.forms import ModelForm

from blogs.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['left', 'right', 'level', 'alias', 'checked_out_by', 'checked_out_at', 'created_by', 'created_at',
                   'modified_by', 'modified_at']
