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

    def get(self, request, pk):
        if not pk:
            return redirect('adminAddUser')
        user_service = UserService()
        user = user_service.getById(pk)
        user_form = UserUpdateForm(instance=user)
        user_groups = user_form['groups']
        user_permissions = user_form['user_permissions']
        # permission=user_form['user_permissions']
        # print(permission)

        post_data = user_service.getPostData(vars(user), None)

        return render(request, 'admin/users/add_user.html',
                      {'postData': post_data, 'user_groups': user_groups, 'user_permissions': user_permissions})

    def post(self, request, pk):
        _post_data = request.POST
        user_groups_input = _post_data.getlist('groups')
        user_permissions_input = _post_data.getlist('user_permissions')

        post_data = _post_data.dict()
        # if "groups" in post_data:
        #     post_data.pop('groups')
        # if "user_permissions" in post_data:
        #     post_data.pop('user_permissions')
        post_data.pop('csrfmiddlewaretoken')
        user_service = UserService()
        post_data['lat'] = round(float(post_data['lat']), 8)
        post_data['lng'] = round(float(post_data['lng']), 8)
        post_data['is_superuser'] = True if (post_data['is_superuser'] == 'True') else False
        post_data['is_staff'] = True if (post_data['is_staff'] == 'True') else False
        post_data['is_active'] = True if (post_data['is_active'] == 'True') else False
        post_data['phone_activated'] = True if (post_data['phone_activated'] == 'True') else False
        post_data['sendEmail'] = True if (post_data['sendEmail'] == 'True') else False
        post_data['sendSMS'] = True if (post_data['sendSMS'] == 'True') else False

        try:
            if "image" in post_data:
                post_data.pop('image')
            # if "groups" in post_data:
            #     post_data.pop('groups')
            # if "user_permissions" in post_data:
            #     post_data.pop('user_permissions')
            if "is_superuser_chkbox" in post_data:
                post_data.pop('is_superuser_chkbox')
            if "is_staff_chkbox" in post_data:
                post_data.pop('is_staff_chkbox')
            if "is_active_chkbox" in post_data:
                post_data.pop('is_active_chkbox')
            if "phone_activated_chkbox" in post_data:
                post_data.pop('phone_activated_chkbox')
            if "sendEmail_chkbox" in post_data:
                post_data.pop('sendEmail_chkbox')
            if "sendSMS_chkbox" in post_data:
                post_data.pop('sendSMS_chkbox')
        except Exception as e:
            print('field pop error')
            print(e)

        if not post_data['phone']:
            post_data.pop('phone')

        if pk:
            if not post_data['password']:
                post_data.pop('password')
            user = user_service.getById(pk)
            post_form = UserUpdateForm(post_data, instance=user)
            # print(post_form)
        else:
            user = CustomUser()
            post_form = UserForm(post_data, instance=user)

        user_groups = post_form['groups']
        user_permissions = post_form['user_permissions']
        print(user_groups)
        print(user_permissions)
        if post_form.is_valid():
            status = user_service.saveUser(post_data, pk)
            if status['success']:
                messages.success(request, 'Success')
                return redirect('adminUserDetail', pk=status['id'])
            else:
                messages.error(request, 'Error occurred while saving user')
                post_data['id'] = 0
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
