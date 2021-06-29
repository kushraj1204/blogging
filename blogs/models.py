from django.db import models
from django.db.models import TextField
from django.utils import timezone
from django.utils.text import slugify
from Users.models import CustomUser


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=False)
    left = models.IntegerField(default=0, blank=True)
    right = models.IntegerField(default=0, blank=True)
    level = models.IntegerField(default=0, blank=True)
    title = models.CharField(max_length=200)
    alias = models.SlugField(max_length=200)
    note = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    checked_out_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='category_checked_out_by',
                                       db_column='checked_out_by', null=True, blank=True)
    checked_out_at = models.DateTimeField(auto_now=True)
    metadesc = models.TextField(blank=True, verbose_name='Meta Description')
    metakey = models.TextField(blank=True, verbose_name='Meta Key')
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='category_created_by',
                                   db_column='created_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='category_modified_by',
                                    db_column='modified_by', null=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.parent is not None:
            parent = Category.objects.get(id=self.parent_id)
            self.level = parent.level + 1
        title_trimmed = self.title.strip()
        title = " ".join(title_trimmed.split())
        self.title = title
        if not self.id:
            self.alias = self.generate_alias(self.title)
        self.created_by_id = 1
        self.modified_by_id = 1
        try:
            super(Category, self).save(*args, **kwargs)
            self.category_rebuild()
            return True
        except Exception as e:
            print(e)
            return False

    def generate_alias(self, title):
        alias = slugify(self.title)
        same_alias_category = Category.objects.filter(alias__contains=alias).order_by('-id')
        if (len(same_alias_category) == 0):
            return alias
        else:
            appended_string = ((same_alias_category[0]).alias).replace(alias, '')
            # print(appended_string)
            if (len(appended_string) > 0):
                appended_string = appended_string[1:]
            else:
                appended_string = '0'

            append_number = int(appended_string)
            return alias + '-' + str(append_number + 1)

    def category_rebuild(self, parent_id=None, left=0, level=0):
        children = list(Category.objects.filter(parent_id=parent_id).values().all())
        right = left + 1
        if (len(children) > 0):
            for item in children:
                right = self.category_rebuild(item['id'], right, level + 1)
                if (right == False):
                    return False
        Category.objects.filter(id=parent_id).update(left=left, right=right, level=level)
        return right + 1


class Blog(models.Model):
    title = models.CharField(max_length=200)
    alias = models.SlugField(unique=True, max_length=200)
    introtext = models.CharField(max_length=200, null=True, blank=True, verbose_name='Intro Text')
    tags = models.CharField(max_length=200, null=True, blank=True, verbose_name='Tags')
    displayphoto = models.ImageField(upload_to='blog/static/blog', null=True, blank=True, verbose_name='Display Photo')
    research_data = TextField(default="Research Data")
    fulltext = TextField(null=True, blank=True, verbose_name='Full Text')
    cat_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Category')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_created_by',
                                   db_column='created_by', null=True, )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_modified_by',
                                    db_column='modified_by', null=True)
    checked_out_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_checked_out_by',
                                       db_column='checked_out_by', null=True, blank=True)
    checked_out_time = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name="Published")
    published_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_published_by',
                                     db_column='published_by', null=True, )
    researched = models.BooleanField(default=False, verbose_name="Research completed")
    researched_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_researched_by',
                                      db_column='researched_by', null=True, )
    authored = models.BooleanField(default=False, verbose_name="Authoring completed")
    authored_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_authored_by',
                                    db_column='authored_by', null=True, )
    edited = models.BooleanField(default=False, verbose_name="Editing completed")
    edited_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='blog_edited_by',
                                  db_column='edited_by', null=True, )
    published_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    metakey = models.TextField(blank=True, null=True, verbose_name='Meta Key')
    metadesc = models.TextField(blank=True, null=True, verbose_name='Meta Description')
    hits = models.IntegerField(blank=True, default=0)
    version = models.IntegerField(default=0)
    featured = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        print('save')
        print(not self.id or not self.alias)
        if (not self.id or not self.alias):
            self.alias = self.generate_alias()
        super(Blog, self).save(*args, **kwargs)

    def generate_alias(self):
        alias = slugify(self.title)
        same_alias_blog = Blog.objects.filter(alias__contains=alias).order_by('-id')

        if (len(same_alias_blog) == 0):
            return alias
        else:
            appended_string = ((same_alias_blog[0]).alias).replace(alias, '')
            if (len(appended_string) > 0):
                appended_string = appended_string[1:]
            else:
                appended_string = '0'

            append_number = int(appended_string)
            return alias + '-' + str(append_number + 1)


class Content(models.Model):
    title = models.CharField(max_length=200)
    alias = models.SlugField(unique=True, max_length=200)
    fulltext = TextField(null=True)
    metakey = models.TextField(blank=True, null=True, verbose_name='Meta Key')
    metadesc = models.TextField(blank=True, null=True, verbose_name='Meta Description')

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.alias = self.generate_alias(self.title)
        super(Content, self).save(*args, **kwargs)

    def generate_alias(self, title):
        alias = slugify(self.title)
        same_alias_category = Content.objects.filter(alias__contains=alias).order_by('-id')
        if (len(same_alias_category) == 0):
            return alias
        else:
            appended_string = ((same_alias_category[0]).alias).replace(alias, '')
            if (len(appended_string) > 0):
                appended_string = appended_string[1:]
            else:
                appended_string = '0'

            append_number = int(appended_string)
            return alias + '-' + str(append_number + 1)

