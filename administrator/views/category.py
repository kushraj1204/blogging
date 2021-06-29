from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from administrator.forms import CategoryForm
from administrator.services import CategoryService
from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
import json

from blogs.models import Category


class CategoryView(BaseAdminView):
    category_service = CategoryService()

    @classmethod
    def get_list(cls, request):
        response = cls.pre_function(cls, request, session_menu='Category', session_submenu='',
                                    permissions_required=['blogs.change_category'])
        if not response['status']:
            return response['action']
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        categories = Category.objects.all().filter(
            Q(title__icontains=keyword)).order_by('id')
        paginator = Paginator(categories, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/category/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})

    @classmethod
    def add(cls, request):
        response = cls.pre_function(cls, request, session_menu='Category', session_submenu='',
                                    permissions_required=['blogs.add_category'])
        if not response['status']:
            return response['action']
        if request.method == 'POST':
            _post_data = request.POST
            post_data = _post_data.dict()
            print(post_data)
            post_data.pop('csrfmiddlewaretoken')
            category = Category()
            post_form = CategoryForm(post_data, instance=category)
            if post_form.is_valid():
                status = post_form.save()
                if status:
                    messages.success(request, 'Success')
                    return redirect('adminCategoryDetail', pk=category.pk)
                else:
                    messages.error(request, 'Error occurred while saving category.py')
                    parents = cls.category_service.get_categories(new=True)
                    post_data['id'] = 0
                    post_data = cls.category_service.getPostData(post_data, None)
                    return render(request, 'admin/category/add_category.html',
                                  {'postData': post_data, 'parents': parents})

            else:
                messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
                print(post_form.errors)
                errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
                post_data = cls.category_service.getPostData(post_data, errors)
                parents = cls.category_service.get_categories(new=True)
                print(post_data)
                return render(request, 'admin/category/add_category.html',
                              {'postData': post_data, 'parents': parents})

        else:
            category = Category()
            category.id = 0
            parents = cls.category_service.get_categories(new=True)
            post_data = cls.category_service.getPostData(vars(category), None)
            return render(request, 'admin/category/add_category.html',
                          {'postData': post_data, 'parents': parents})

    @classmethod
    def delete(cls, request, pk):
        response = cls.pre_function(cls, request, session_menu='Category', session_submenu='',
                                    permissions_required=['blogs.delete_category'])
        if not response['status']:
            messages.error(request, 'You are unauthorized to complete this action')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

        if pk == 1:
            messages.error(request, 'Root category.py cannot be altered')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")
        _post_data = request.POST
        try:
            category = get_object_or_404(Category, pk=pk)
            status = category.delete()
        except:
            status = 0
        if status:
            messages.success(request, 'Category Deleted Successfully')
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            messages.error(request, 'There was a problem in deleting the category')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

    def get(self, request, pk):

        if not pk:
            return redirect('adminCategoryAdd')
        response = self.pre_function(request, session_menu='Category', session_submenu='',
                                     permissions_required=['blogs.view_category'])
        if not response['status']:
            return response['action']
        category = get_object_or_404(Category, pk=pk)
        post_data = self.category_service.getPostData(vars(category), None)
        parents = self.category_service.get_categories()
        print(parents)
        return render(request, 'admin/category/add_category.html',
                      {'postData': post_data, 'parents': parents})

    def post(self, request, pk):
        response = self.pre_function(request, session_menu='Category', session_submenu='',
                                     permissions_required=['blogs.change_category'])
        if not response['status']:
            return response['action']
        _post_data = request.POST
        post_data = _post_data.dict()
        post_data.pop('csrfmiddlewaretoken')
        category = get_object_or_404(Category, pk=pk)
        if pk == 1:  # special case for root category edit
            category.metakey = request.POST.get('metakey')
            category.metadesc = request.POST.get('metadesc')
            status = category.save()
            if status:
                messages.success(request, 'Success')
                return redirect('adminCategoryDetail', pk=pk)
            else:
                messages.error(request, 'Error occurred while saving category.py')
                post_data['id'] = pk
                post_data = self.category_service.getPostData(post_data, None)
                parents = self.category_service.get_categories()
                return render(request, 'admin/category/add_category.html',
                              {'postData': post_data, 'parents': parents})

        post_form = CategoryForm(post_data, instance=category)
        if post_form.is_valid():

            status = post_form.save()
            if status:
                messages.success(request, 'Success')
                return redirect('adminCategoryDetail', pk=pk)
            else:
                messages.error(request, 'Error occurred while saving category.py')
                post_data['id'] = pk
                post_data = self.category_service.getPostData(post_data, None)
                parents = self.category_service.get_categories()
                return render(request, 'admin/category/add_category.html',
                              {'postData': post_data, 'parents': parents})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            print(post_form.errors.as_json())
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = self.category_service.getPostData(post_data, errors)
            parents = self.category_service.get_categories()
            return render(request, 'admin/category/add_category.html',
                          {'postData': post_data, 'parents': parents})
