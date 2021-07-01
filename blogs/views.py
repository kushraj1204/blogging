from django.core.paginator import Paginator
from blogs.models import Category, Blog, Content
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from datetime import datetime, timedelta
from administrator.models import Settings
from blogs.utils import getImages


class SiteView(View):
    settings = get_object_or_404(Settings, pk=1)
    last_week = datetime.today() - timedelta(days=7)
    categories = Category.objects.all().filter(level=2).filter(published=1)
    explore_blogs = Blog.objects.all().filter(published=1, cat_id__published=1)[:settings.page_limit]
    recommended = Blog.objects.all().filter(published=1, cat_id__published=1, published_date__gte=last_week).order_by(
        'hits')[:settings.page_limit]

    @classmethod
    def home(cls, request):
        print(cls.settings.page_limit)
        keyword = request.GET.get('keyword')
        keyword = keyword if keyword is not None else ""
        blogs = Blog.objects.all().filter(published=1, cat_id__published=1, title__icontains=keyword).order_by('id')
        paginator = Paginator(blogs, cls.settings.page_limit)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for blog in page_obj:
            blog.displayphoto_options = getImages(str(blog.displayphoto))
        context = {"explore": cls.explore_blogs,
                   "categories": cls.categories,
                   "recommended": cls.recommended,
                   "category_id": 0,
                   "page_obj": page_obj,
                   "metadescription": cls.settings.metadesc,
                   "metakey": cls.settings.metakey,
                   "searchkeyword": keyword,
                   "pagetitle": "Home"}
        return render(request, "blog/blogs.html", context)

    @classmethod
    def blogs_by_category(cls, request, slug):
        category = Category.objects.filter(published=1).get(alias=slug)
        blogs = Blog.objects.all().filter(cat_id__alias=slug, cat_id__published=1, published=1).order_by('id')
        paginator = Paginator(blogs, cls.settings.page_limit)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for blog in page_obj:
            blog.displayphoto_options = getImages(str(blog.displayphoto))
        top_blogs = Blog.objects.all().filter(cat_id=category.id)[:5]
        metakeywords = category.metakey
        metadescription = category.metadesc
        context = {"categories": cls.categories,
                   "blogs": blogs,
                   "category_name": category.title,
                   "category_id": category.id,
                   "category_slug": slug,
                   "topblogs": top_blogs,
                   "recommended": cls.recommended,
                   "explore": cls.explore_blogs,
                   "page_obj": page_obj,
                   "metadescription": metadescription,
                   "pagetitle": category.title,
                   "metakey": metakeywords}
        return render(request, "blog/blogs.html", context)

    @classmethod
    def blogs_by_tag(cls, request, slug):

        blogs = Blog.objects.all().filter(cat_id__published=1, published=1, tags__contains=slug).order_by('id')
        paginator = Paginator(blogs, cls.settings.page_limit)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for blog in page_obj:
            blog.displayphoto_options = getImages(str(blog.displayphoto))

        context = {"categories": cls.categories,
                   "blogs": blogs,
                   "category_name": slug,
                   "category_slug": slug,
                   "recommended": cls.recommended,
                   "explore": cls.explore_blogs,
                   "page_obj": page_obj,
                   "metadescription": cls.settings.metadesc,
                   "pagetitle": slug,
                   "metakey": cls.settings.metakey}
        return render(request, "blog/blogs.html", context)

    @classmethod
    def getBlog(cls, request, slug):
        blog = Blog.objects.filter(published=1, cat_id__published=1).get(alias=slug)
        blog.hits = blog.hits + 1
        blog.save()
        displayphoto_options = getImages(str(blog.displayphoto))
        blog.displayphoto_options = displayphoto_options
        if blog.tags:
            blog.tags = blog.tags.split(",")
        category_slug = blog.cat_id.alias
        metakey = cls.settings.metakey
        metakey = metakey if metakey else ''
        metakey = slug if metakey == '' else metakey + ',' + slug
        context = {"categories": cls.categories,
                   "recommended": cls.recommended,
                   "blog": blog,
                   "category_slug": category_slug,
                   "category_id": blog.cat_id_id,
                   "explore": cls.explore_blogs,
                   "metadescription": cls.settings.metadesc,
                   "metakey": metakey,
                   "pagetitle": blog.title
                   }
        return render(request, "blog/blog.html", context)

    @classmethod
    def getContent(cls, request, slug):
        content = Content.objects.get(alias=slug)
        context = {"categories": cls.categories,
                   "recommended": cls.recommended,
                   "content": content,
                   "explore": cls.explore_blogs,
                   "pagetitle": content.title,
                   "metadescription": content.metadesc,
                   "metakey": content.metakey}
        return render(request, "blog/content.html", context)
