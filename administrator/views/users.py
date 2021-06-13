from django.http import HttpResponse
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
    def add_user(cls, request):
        user = CustomUser()
        user.id = 0
        user_service = UserService()
        post_data = user_service.getPostData(vars(user), None)
        return render(request, 'admin/users/add_user.html',
                      {'postData': post_data, 'user_groups': None, 'user_permissions': None})

    @classmethod
    def delete_user(cls, request):
        _post_data = request.POST
        pk = _post_data.get('id')
        user = CustomUser.objects.get(pk=pk)
        status = user.delete()
        if status:
            messages.success(request, 'Group Deleted Successfully')
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            messages.error(request, 'There was a problem in deleting the group')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

    def get(self, request, pk):
        if not pk:
            return redirect('adminAddUser')
        user_service = UserService()
        user = user_service.getById(pk)
        user_form = UserUpdateForm(instance=user)
        user_groups = user_form['groups']
        user_permissions = user_form['user_permissions']

        post_data = user_service.getPostData(vars(user), None)

        return render(request, 'admin/users/add_user.html',
                      {'postData': post_data, 'user_groups': user_groups, 'user_permissions': user_permissions})

    def post(self, request, pk):
        user_service = UserService()
        _post_data = request.POST
        user_permissions_input = _post_data.getlist('user_permissions')
        user_groups_input = _post_data.getlist('groups')
        _user_permissions = []
        _user_groups = []
        for x in user_groups_input:
            _user_groups.append(x)
        for x in user_permissions_input:
            _user_permissions.append(x)

        post_data = _post_data.dict()
        post_data = self.get_filtered_input(post_data)
        print('filtered input')
        print(_user_permissions)
        print(_user_groups)
        post_data['groups'] = _user_groups
        post_data['user_permissions'] = _user_permissions

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

        user_groups = post_form['groups']
        user_permissions = post_form['user_permissions']
        if post_form.is_valid():
            status = user_service.saveUser(post_data, pk)
            if status['success']:
                messages.success(request, 'Success')
                return redirect('adminUserDetail', pk=status['id'])
            else:
                messages.error(request, 'Error occurred while saving user')
                post_data['id'] = pk
                post_data = user_service.getPostData(post_data, None)
                return render(request, 'admin/users/add_user.html',
                              {'postData': post_data, 'user_groups': user_groups, 'user_permissions': user_permissions})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            print(post_form.errors)
            print(errors)
            post_data = user_service.getPostData(post_data, errors)
            return render(request, 'admin/users/add_user.html',
                          {'postData': post_data, 'user_groups': user_groups, 'user_permissions': user_permissions})

    def get_filtered_input(self, post_data):
        return_data = dict()
        return_data['id'] = post_data['id']
        return_data['first_name'] = post_data['first_name']
        return_data['last_name'] = post_data['last_name']
        return_data['gender'] = post_data['gender']
        return_data['phone'] = post_data['phone']
        return_data['dob'] = post_data['dob']
        return_data['address'] = post_data['address']
        return_data['lat'] = round(float(post_data['lat']), 8)
        return_data['lng'] = round(float(post_data['lng']), 8)
        return_data['profile_image'] = post_data['profile_image']
        return_data['email'] = post_data['email']
        return_data['username'] = post_data['username']
        return_data['password'] = post_data['password']
        return_data['is_superuser'] = True if (post_data['is_superuser'] == 'True') else False
        return_data['is_staff'] = True if (post_data['is_staff'] == 'True') else False
        return_data['is_active'] = True if (post_data['is_active'] == 'True') else False
        return_data['phone_activated'] = True if (post_data['phone_activated'] == 'True') else False
        return_data['sendEmail'] = True if (post_data['sendEmail'] == 'True') else False
        return_data['sendSMS'] = True if (post_data['sendSMS'] == 'True') else False
        return return_data
