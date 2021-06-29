from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from administrator.forms import BlogForm
from administrator.services import BlogService, CategoryService
from administrator.views.base import BaseAdminView
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
import json

from blogs.models import Blog


class BlogView(BaseAdminView):
    blog_service = BlogService()
    category_service = CategoryService()

    @classmethod
    def get_list(cls, request):
        response = cls.pre_function(cls, request, session_menu='Blog', session_submenu='',
                                    permissions_required=['blogs.view_blog'])
        if not response['status']:
            return response['action']
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        blogs = Blog.objects.all().filter(
            Q(title__icontains=keyword)).order_by('published','edited','authored','researched','-id')
        paginator = Paginator(blogs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/blog/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})

    @classmethod
    def add(cls, request):
        response = cls.pre_function(cls, request, session_menu='Blog', session_submenu='',
                                    permissions_required=['blogs.add_blog'])
        if not response['status']:
            return response['action']
        if request.method == 'POST':
            _post_data = request.POST
            post_data = _post_data.dict()
            blog = Blog()
            loggedInUser = request.session.get('loggedInUser')
            post_data = cls.get_filtered_input(post_data, loggedInUser, blog, permissions=cls.userpermissions,
                                               groups=cls.groups)
            post_form = BlogForm(post_data, instance=blog)
            if post_form.is_valid():
                status = cls.blog_service.saveBlog(post_data, blog=blog)
                print(status)
                print('result')
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
        response = cls.pre_function(cls, request, session_menu='Blog', session_submenu='',
                                    permissions_required=['blogs.delete_blog'])
        if not response['status']:
            messages.error(request, 'You are unauthorized to complete this action')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")
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
        response = self.pre_function(request, session_menu='Blog', session_submenu='',
                                     permissions_required=['blogs.view_blog'])
        if not response['status']:
            return response['action']
        blog = get_object_or_404(Blog, pk=pk)
        post_data = self.blog_service.getPostData(vars(blog), None)
        categories = self.category_service.get_categories(getRoot=False)
        return render(request, 'admin/blog/add_blog.html',
                      {'postData': post_data, 'categories': categories})

    def post(self, request, pk):
        response = self.pre_function(request, session_menu='Blog', session_submenu='',
                                     permissions_required=['blogs.change_blog'])
        if not response['status']:
            return response['action']
        _post_data = request.POST
        post_data = _post_data.dict()
        loggedInUser = request.session.get('loggedInUser')
        blog = get_object_or_404(Blog, pk=pk)
        post_data = self.get_filtered_input(post_data, loggedInUser, blog, permissions=self.userpermissions,
                                            groups=self.groups)
        if post_data['version'] != blog.version:
            messages.error(request,
                           'This article has been updated in the mean time. Proceed only if you want to override the newly saved article')
            post_data['id'] = pk
            post_data['version'] = blog.version
            categories = self.category_service.get_categories(getRoot=False)
            post_data = self.blog_service.getPostData(post_data, None)
            return render(request, 'admin/blog/add_blog.html',
                          {'postData': post_data, 'categories': categories})

        post_form = BlogForm(post_data, instance=blog)
        if post_form.is_valid():
            status = self.blog_service.saveBlog(post_data, pk=pk, blog=blog)
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
    def get_filtered_input(post_data, _loggedInUser, blog, groups=[], permissions={}):
        loggedInUser = _loggedInUser['id']
        return_data = dict()
        return_data['title'] = post_data['title']
        return_data['introtext'] = post_data['introtext']
        return_data['displayphoto'] = post_data['displayphoto']
        return_data['research_data'] = post_data['research_data']
        return_data['fulltext'] = post_data['fulltext']
        return_data['cat_id'] = int(post_data['cat_id'])
        return_data['metakey'] = post_data['metakey']
        return_data['metadesc'] = post_data['metadesc']
        return_data['researched'] = True if (post_data['researched'] == 'True') else False
        return_data['authored'] = True if (post_data['authored'] == 'True') else False
        return_data['edited'] = True if (post_data['edited'] == 'True') else False
        return_data['published'] = True if (post_data['published'] == 'True') else False
        return_data['version'] = int(post_data['version'])
        if not blog.id:
            return_data['version'] = 1
        if return_data['researched'] and not blog.researched:
            return_data['researched_by_id'] = loggedInUser
            if 2 not in groups and not _loggedInUser['is_superuser']:
                return_data['researched_by_id'] = None
                return_data['researched'] = False
        if return_data['authored'] and not blog.authored:
            return_data['authored_by_id'] = loggedInUser
            if (3 not in groups and not _loggedInUser['is_superuser']) or not return_data['researched']:
                return_data['authored_by_id'] = None
                return_data['authored'] = False
        if return_data['edited'] and not blog.edited:
            return_data['edited_by_id'] = loggedInUser
            if (4 not in groups and not _loggedInUser['is_superuser']) or not return_data['authored']:
                return_data['edited_by_id'] = None
                return_data['edited'] = False
        if return_data['published'] and not blog.published or not _loggedInUser['is_superuser']:
            return_data['published_by_id'] = loggedInUser
            return_data['published_date'] = timezone.now()
            if (5 not in groups and not _loggedInUser['is_superuser']) or not return_data['edited']:
                return_data['published_by_id'] = None
                return_data['published'] = False
        if not blog.id:
            return_data['created_by_id'] = loggedInUser

        if not bool(set([3, 4, 5]) & set(groups)) and not _loggedInUser['is_superuser']:
            return_data.pop('fulltext')

        return_data['featured'] = True if (post_data['featured'] == 'True') else False
        return_data['modified_by_id'] = loggedInUser
        tags = post_data['tags']
        return_data['tags'] = tags
        if tags:
            tags = tags.split(",")
            for index, tag in enumerate(tags):
                tag = tag.strip()
                tag = slugify(tag.lower())
                tags[index] = tag
            return_data['tags'] = ','.join(tags)
        print(return_data)
        return return_data
