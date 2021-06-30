from django.contrib.auth.models import Permission
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from ..forms import PermissionForm
import json


class PermissionsView(BaseAdminView):

    @classmethod
    def get_list(cls, request):
        response = cls.pre_function(cls, request, session_menu='Permissions', session_submenu='',
                                    permissions_required=[], must_be_superuser=True)
        if not response['status']:
            return response['action']
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        permissions = Permission.objects.filter(
            Q(codename__icontains=keyword)).order_by('-id')
        paginator = Paginator(permissions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/permissions/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})

    def get(self, request):
        response = self.pre_function(request, session_menu='Permissions', session_submenu='',
                                     permissions_required=[], must_be_superuser=True)
        if not response['status']:
            return response['action']
        permission = Permission()
        permission.id = 0
        user_service = UserService()
        content_types = ContentType.objects.all()
        post_data = user_service.getPostData(vars(permission), None)
        return render(request, 'admin/permissions/add_permission.html',
                      {'postData': post_data, 'content_types': content_types})

    def post(self, request):
        response = self.pre_function(request, session_menu='Permissions', session_submenu='',
                                     permissions_required=[])
        if not response['status']:
            return response['action']
        _post_data = request.POST
        post_data = _post_data.dict()
        post_data.pop('csrfmiddlewaretoken')
        print(post_data)
        user_service = UserService()
        permission = Permission()
        post_form = PermissionForm(post_data, instance=permission)
        if post_form.is_valid():
            status = post_form.save()
            if status:
                messages.success(request, 'Success')
                return redirect('adminPermissions')
            else:
                messages.error(request, 'Error occurred while saving settings')
                content_types = ContentType.objects.all()
                post_data = user_service.getPostData(post_data, None)
                return render(request, 'admin/permissions/add_permission.html',
                              {'postData': post_data, 'content_types': content_types})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = user_service.getPostData(post_data, errors)
            content_types = ContentType.objects.all()
            return render(request, 'admin/permissions/add_permission.html',
                          {'postData': post_data, 'content_types': content_types})
