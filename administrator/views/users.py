from django.shortcuts import redirect, render

from Users.models import CustomUser
from administrator.forms import UserForm, UserUpdateForm
from administrator.services.auth import AuthService

from django.core.paginator import Paginator
from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
import json


class Users(BaseAdminView):

    def get(self, request):
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        user_service = UserService()
        users = user_service.getAll(keyword)
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/users/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})


class User(BaseAdminView):

    @classmethod
    def add_user(self, request):
        user = CustomUser()
        user.id = 0
        user_service = UserService()
        post_data = user_service.getPostData(vars(user), None)
        return render(request, 'admin/users/add_user.html',
                      {'postData': post_data})

    def get(self, request, pk):
        if not pk:
            return redirect('adminAddUser')
        user_service = UserService()
        user = user_service.getById(pk)
        post_data = user_service.getPostData(vars(user), None)
        return render(request, 'admin/users/add_user.html',
                      {'postData': post_data})

    def post(self, request, pk):
        _post_data = request.POST
        post_data = _post_data.dict()
        print(post_data)
        post_data.pop('csrfmiddlewaretoken')
        user_service = UserService()
        if not post_data['phone']:
            post_data.pop('phone')
        if pk:
            if not post_data['password']:
                post_data.pop('password')
            user = user_service.getById(pk)
            post_form = UserUpdateForm(post_data, instance=user)
        else:
            user = CustomUser()
            post_form = UserForm(post_data, instance=user)

        if post_form.is_valid():
            status = user_service.saveUser(post_data, pk)
            if status:
                messages.success(request, 'Success')
                # return redirect('adminUserDetail', pk=pk if pk else status)
                return render(request, 'admin/users/add_user.html', {'postData': post_data})
            else:
                messages.error(request, 'Error occurred while saving user')
                return render(request, 'admin/users/add_user.html', {'postData': post_data})

        else:
            print(post_form.errors)
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = user_service.getPostData(post_data, errors)
            return render(request, 'admin/users/add_user.html', {'postData': post_data})
