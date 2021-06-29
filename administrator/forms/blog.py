from django.forms import ModelForm

from blogs.models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ['displayphoto', 'alias', 'checked_out_by', 'checked_out_at', 'created_by', 'created_at',
                   'modified_by', 'modified_at', 'published_by', 'researched_by', 'authored_by', 'edited_by',
                   'published_date', 'hits']
