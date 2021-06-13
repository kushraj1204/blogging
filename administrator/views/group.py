import ast

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from Users.models import CustomUser
from administrator.forms import UserForm, UserUpdateForm, GroupForm
from django.db.models import Q

from django.core.paginator import Paginator
from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
import json
from django.contrib.auth.models import Group


class GroupsView(BaseAdminView):

    def get(self, request):
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        groups = Group.objects.all().filter(
            Q(name__icontains=keyword)).order_by('-id')
        paginator = Paginator(groups, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/groups/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})


class GroupView(BaseAdminView):

    @classmethod
    def add_group(cls, request):
        group = Group()
        group_form = GroupForm(instance=group)
        print(group_form)
        group.id = 0
        user_service = UserService()
        post_data = user_service.getPostData(vars(group), None)
        return render(request, 'admin/groups/add_group.html',
                      {'postData': post_data, 'group_permissions': None})

    @classmethod
    def delete_group(cls, request):
        _post_data = request.POST
        pk = _post_data.get('id')
        group = Group.objects.get(pk=pk)
        status = group.delete()
        if status:
            messages.success(request, 'Group Deleted Successfully')
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            messages.error(request, 'There was a problem in deleting the group')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

    def get(self, request, pk):
        if not pk:
            return redirect('adminAddGroup')
        user_service = UserService()
        group = get_object_or_404(Group, pk=pk)
        group_form = GroupForm(instance=group)
        permissions = group_form['permissions']

        post_data = user_service.getPostData(vars(group), None)

        return render(request, 'admin/groups/add_group.html',
                      {'postData': post_data, 'permissions': permissions})

    def post(self, request, pk):
        _post_data = request.POST
        permissions_input = _post_data.getlist('permissions')
        _permissions = []
        for x in permissions_input:
            _permissions.append(x)

        post_data = _post_data.dict()
        post_data['permissions'] = _permissions
        post_data.pop('csrfmiddlewaretoken')
        user_service = UserService()
        if pk:
            group = get_object_or_404(Group, pk=pk)
            post_form = GroupForm(post_data, instance=group)
        else:
            group = Group()
            post_form = GroupForm(post_data, instance=group)
        permissions = post_form['permissions']
        if post_form.is_valid():
            status = post_form.save()

            if status:
                messages.success(request, 'Success')
                return redirect('adminGroupDetail', pk=pk if pk > 0 else group.pk)
            else:
                messages.error(request, 'Error occurred while saving group')
                post_data['id'] = pk
                post_data = user_service.getPostData(post_data, None)
                return render(request, 'admin/groups/add_group.html',
                              {'postData': post_data, 'permissions': permissions if pk > 0 else None})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            print(post_form.errors)
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = user_service.getPostData(post_data, errors)
            return render(request, 'admin/groups/add_group.html',
                          {'postData': post_data, 'permissions': permissions if pk > 0 else None})
