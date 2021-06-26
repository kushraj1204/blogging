from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from blogs.models import Category, Blog,   Content
from django.contrib import messages
from django.utils.text import slugify
import datetime


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "parent",
                    "title",
                    "note",
                    "description",
                    "published",
                    "metadesc",
                    "metakey",
                )
            },
        ),
    )


class BlogImagesAdmin(admin.ModelAdmin):
    readonly_fields = ["displayimage"]

    def displayimage(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.photo.url if obj.photo else '',
            width='150px',
            height='150px',
        )
        )

    def display_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.photo.url if obj.photo else '',
            width='50px',
            height='50px',
        )
        )

    list_display = ('display_image', 'name')


class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "cat_id",
                    "research_data",
                    "introtext",
                    "displayphoto",
                    "displayimage",
                    "fulltext",
                    "metakey",
                    "metadesc",
                    "researched",
                    "authored",
                    "edited",
                    "published",

                )
            },
        ),
    )

    readonly_fields = ["displayimage"]

    def displayimage(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.displayphoto.url if obj.displayphoto else '',
            width='150px',
            height='150px',
        )
        )

    def display_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.displayphoto.url if obj.displayphoto else '',
            width='50px',
            height='50px',
        )
        )

    list_display = ('title', 'display_image', 'researched', 'authored', 'edited', 'published')

    def generate_alias(self, title):
        alias = slugify(title)
        same_title_blog = Blog.objects.filter(title=title).order_by('-id')
        if (len(same_title_blog) == 0):
            return alias
        else:
            appended_string = ((same_title_blog[0]).alias).replace(alias, '')
            if (len(appended_string) > 0):
                appended_string = appended_string[1:]
            else:
                appended_string = '0'
            append_number = int(appended_string)
            return alias + '-' + str(append_number + 1)

    def save_model(self, request, obj, form, change):
        title_trimmed = obj.title.strip()
        title = " ".join(title_trimmed.split())
        obj.title = title
        if 'title' in form.changed_data:
            obj.alias = self.generate_alias(obj.title)
        user_groups = []
        for g in request.user.groups.all():
            user_groups.append(g.id)

        if request.user.is_superuser:
            user_groups = [1, 2, 3, 4]

        if obj.id is None:  # creation custom logic
            obj.created_by = request.user

        obj.modified_by = request.user
        if 2 not in user_groups:  # 2 indicates researcher
            if obj.researched:
                if 'researched' in form.changed_data:
                    messages.add_message(request, messages.WARNING,
                                         'You do not have permissions to change the researched state')
            obj.researched = False

        if obj.researched:
            obj.researched_by = request.user

        if 1 not in user_groups:  # 1 indicates author
            if obj.authored:
                if 'authored' in form.changed_data:
                    messages.add_message(request, messages.WARNING,
                                         'You do not have permissions to change the authored state')
            obj.authored = False

        if obj.authored:
            obj.authored_by = request.user

        if 3 not in user_groups:  # 3 indicates editor
            if obj.edited:
                if 'edited' in form.changed_data:
                    messages.add_message(request, messages.WARNING,
                                         'You do not have permissions to change the edited state')
            obj.edited = False

        if obj.edited:
            obj.edited_by = request.user

        if 4 not in user_groups:  # 3 indicates editor
            if obj.published:
                if 'published' in form.changed_data:
                    messages.add_message(request, messages.WARNING,
                                         'You do not have permissions to change the published state')
            obj.published = False

        if obj.published:
            obj.published_date = datetime.datetime.now()
            obj.published_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)








class ArticleAdmin(admin.ModelAdmin):

    def generate_alias(self, title):
        alias = slugify(title)
        same_title_blog = Content.objects.filter(title=title).order_by('-id')
        if (len(same_title_blog) == 0):
            return alias
        else:
            appended_string = ((same_title_blog[0]).alias).replace(alias, '')
            if (len(appended_string) > 0):
                appended_string = appended_string[1:]
            else:
                appended_string = '0'
            append_number = int(appended_string)
            return alias + '-' + str(append_number + 1)

    def save_model(self, request, obj, form, change):
        title_trimmed = obj.title.strip()
        title = " ".join(title_trimmed.split())
        obj.title = title
        if 'title' in form.changed_data:
            obj.alias = self.generate_alias(obj.title)

        super().save_model(request, obj, form, change)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "fulltext",
                    "metakey",
                    "metadesc"
                )
            },
        ),
    )


admin.site.register(Content, ArticleAdmin)
