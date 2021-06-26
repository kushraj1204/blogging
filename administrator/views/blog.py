from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from administrator.forms import BlogForm
from administrator.services import BlogService, CategoryService
from administrator.views.base import BaseAdminView
from django.contrib import messages
import json

from blogs.models import Blog


class BlogView(BaseAdminView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs, session_menu='Blog', session_submenu='',
                                permission_required=[])

    blog_service = BlogService()
    category_service = CategoryService()

    @classmethod
    def get_list(cls, request):
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        blogs = Blog.objects.all().filter(
            Q(title__icontains=keyword)).order_by('id')
        paginator = Paginator(blogs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/blog/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})

    @classmethod
    def add(cls, request):
        if request.method == 'POST':
            _post_data = request.POST
            post_data = _post_data.dict()
            post_data = cls.get_filtered_input(post_data)
            blog = Blog()
            post_form = BlogForm(post_data, instance=blog)
            if post_form.is_valid():
                status = cls.blog_service.saveBlog(post_data, loggedInuser=cls.loggedInUser)
                if status['success']:
                    messages.success(request, 'Success')
                    return redirect('adminBlogDetail', pk=status['id'])
                else:
                    messages.error(request, 'Error occurred while saving blog')
                    post_data['id'] = 0
                    categories = cls.category_service.get_categories(getRoot=False)
                    post_data = cls.blog_service.getPostData(post_data, None)
                    return render(request, 'admin/blog/add_blog.html',
                                  {'postData': post_data, 'categories': categories})

            else:
                messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
                print(post_form.errors.as_json())
                errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
                categories = cls.category_service.get_categories(getRoot=False)
                post_data = cls.blog_service.getPostData(post_data, errors)
                return render(request, 'admin/blog/add_blog.html',
                              {'postData': post_data, 'categories': categories})

        else:
            blog = Blog()
            blog.id = 0
            categories = cls.category_service.get_categories(getRoot=False)
            post_data = cls.blog_service.getPostData(vars(blog), None)
            return render(request, 'admin/blog/add_blog.html',
                          {'postData': post_data, 'categories': categories})

    @classmethod
    def delete(cls, request, pk):
        _post_data = request.POST
        try:
            blog = get_object_or_404(Blog, pk=pk)
            status = blog.delete()
        except:
            status = 0
        if status:
            messages.success(request, 'Blog Deleted Successfully')
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            messages.error(request, 'There was a problem in deleting the blog')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

    def get(self, request, pk):
        if not pk:
            return redirect('adminBlogAdd')
        blog = get_object_or_404(Blog, pk=pk)
        post_data = self.blog_service.getPostData(vars(blog), None)
        categories = self.category_service.get_categories(getRoot=False)
        return render(request, 'admin/blog/add_blog.html',
                      {'postData': post_data, 'categories': categories})

    def post(self, request, pk):
        _post_data = request.POST
        post_data = _post_data.dict()
        post_data = self.get_filtered_input(post_data)

        blog = get_object_or_404(Blog, pk=pk)
        post_form = BlogForm(post_data, instance=blog)
        if post_form.is_valid():
            status = self.blog_service.saveBlog(post_data, pk, self.loggedInUser)
            if status:
                messages.success(request, 'Success')
                return redirect('adminBlogDetail', pk=pk)
            else:
                messages.error(request, 'Error occurred while saving blog')
                post_data['id'] = pk
                categories = self.category_service.get_categories(getRoot=False)
                post_data = self.blog_service.getPostData(post_data, None)
                return render(request, 'admin/blog/add_blog.html',
                              {'postData': post_data, 'categories': categories})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            print(post_form.errors)
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = self.blog_service.getPostData(post_data, errors)
            categories = self.category_service.get_categories(getRoot=False)
            return render(request, 'admin/blog/add_blog.html',
                          {'postData': post_data, 'categories': categories})

    @staticmethod
    def get_filtered_input(post_data):
        return_data = dict()
        return_data['title'] = post_data['title']
        return_data['introtext'] = post_data['introtext']
        return_data['displayphoto'] = post_data['displayphoto']
        return_data['research_data'] = post_data['research_data']
        return_data['fulltext'] = post_data['fulltext']
        return_data['cat_id'] = int(post_data['cat_id'])
        return_data['metakey'] = post_data['metakey']
        return_data['metadesc'] = post_data['metadesc']
        return_data['published'] = True if (post_data['published'] == 'True') else False
        return_data['featured'] = True if (post_data['featured'] == 'True') else False
        return return_data
