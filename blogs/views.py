from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.translation import gettext

# Create your views here.
from blogs.models import Category, Blog


def home(request):
    categories = Category.objects.all().filter(level=2)
    blogs = Blog.objects.all()[:10]
    metakeywords = ""
    metadescription = ""
    context = {"test": gettext("Test"), "categories": categories, "category_id": 0, "page_obj": blogs,
               "metadescription": metadescription,
               "metakey": metakeywords}
    return render(request, "blog/blogs.html", context)


def blogs_by_category(request, slug):
    category = Category.objects.get(alias=slug)
    blogs = Blog.objects.all().filter(cat_id=category.id).order_by('id')
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for article in page_obj:
        if not (article.displayphoto):
            article.displayphoto = 'blog/static/blog/Capture.jpg'
    top_blogs = Blog.objects.all().filter(cat_id=category.id)[:5]
    explore_blogs = Blog.objects.all()[:10]
    categories = Category.objects.all().filter(level=2)
    metakeywords = category.metakey
    metadescription = category.metadesc
    context = {"categories": categories, "blogs": blogs, "category_name": category.title, "category_id": category.id,
               "topblogs": top_blogs,
               "explore": explore_blogs, "page_obj": page_obj, "metadescription": metadescription,
               "metakey": metakeywords}
    return render(request, "blog/blogs.html", context)


def getBlog(request, slug):
    categories = Category.objects.all().filter(level=2)
    blog = Blog.objects.get(alias=slug)
    metakeywords = blog.metakey
    metadescription = blog.metadesc
    context = {"categories": categories, "blog": blog, "category_id": blog.cat_id_id,
               "metadescription": metadescription, "metakey": metakeywords}
    return render(request, "blog/blog.html", context)
