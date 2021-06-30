from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from administrator.forms import GroupForm
from django.db.models import Q
from django.core.paginator import Paginator
from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
import json
from django.contrib.auth.models import Group


class GroupView(BaseAdminView):

    @classmethod
    def get_list(cls, request):
        response = cls.pre_function(cls, request, session_menu='Group', session_submenu='',
                                    permissions_required=['auth.view_group'])
        if not response['status']:
            return response['action']
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

    @classmethod
    def add(cls, request):
        response = cls.pre_function(cls, request, session_menu='Group', session_submenu='',
                                    permissions_required=['auth.add_group'])
        if not response['status']:
            return response['action']
        if request.method == 'POST':
            _post_data = request.POST
            post_data = _post_data.dict()
            post_data.pop('csrfmiddlewaretoken')
            user_service = UserService()
            group = Group()
            post_form = GroupForm(post_data, instance=group)
            if post_form.is_valid():
                status = post_form.save()
                if status:
                    cls.log_to_admin(cls, modelname='group', object_id=group.pk, object_repr=post_data['title'],
                                     action_flag=1,
                                     change_message=json.dumps([{'added': {}}]))
                    messages.success(request, 'Success')
                    return redirect('adminGroupDetail', pk=group.pk)
                else:
                    messages.error(request, 'Error occurred while saving group')
                    post_data['id'] = 0
                    post_data = user_service.getPostData(post_data, None)
                    return render(request, 'admin/groups/add_group.html',
                                  {'postData': post_data, 'permissions': None})

            else:
                messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
                print(post_form.errors)
                errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
                post_data = user_service.getPostData(post_data, errors)
                return render(request, 'admin/groups/add_group.html',
                              {'postData': post_data, 'permissions': None})

        else:
            group = Group()
            group.id = 0
            user_service = UserService()
            post_data = user_service.getPostData(vars(group), None)
            return render(request, 'admin/groups/add_group.html',
                          {'postData': post_data, 'group_permissions': None})

    @classmethod
    def delete(cls, request, pk):
        response = cls.pre_function(cls, request, session_menu='Group', session_submenu='',
                                    permissions_required=['auth.delete_group'])
        if not response['status']:
            messages.error(request, 'You are unauthorized to complete this action')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

        if request.method == 'POST':
            _post_data = request.POST
            try:
                group = get_object_or_404(Group, pk=pk)
                status = group.delete()
            except:
                status = 0
            if status:
                cls.log_to_admin(cls, modelname='group', object_id=pk, object_repr=group.__str__(), action_flag=3,
                                 change_message=json.dumps([{'deleted': {}}]))

                messages.success(request, 'Group Deleted Successfully')
                return HttpResponse(json.dumps({'success': True}), content_type="application/json")
            else:
                messages.error(request, 'There was a problem in deleting the group')
                return HttpResponse(json.dumps({'success': False}), content_type="application/json")
        else:
            return redirect('adminGroupDetail', pk=pk)

    def get(self, request, pk):
        response = self.pre_function(request, session_menu='Group', session_submenu='',
                                     permissions_required=['auth.view_group'])
        if not response['status']:
            return response['action']
        if not pk:
            return redirect('adminGroupAdd')
        user_service = UserService()
        group = get_object_or_404(Group, pk=pk)
        group_form = GroupForm(instance=group)
        permissions = group_form['permissions']

        post_data = user_service.getPostData(vars(group), None)

        return render(request, 'admin/groups/add_group.html',
                      {'postData': post_data, 'permissions': permissions})

    def post(self, request, pk):
        response = self.pre_function(request, session_menu='Group', session_submenu='',
                                     permissions_required=['auth.change_group'])
        if not response['status']:
            return response['action']
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
                changed_fields = self.getChangedFields(post_data, group)
                if len(changed_fields) > 0:
                    self.log_to_admin(modelname='group', object_id=pk, object_repr=group.__str__(), action_flag=2,
                                      change_message=json.dumps([{'changed': {'fields': changed_fields}}]))

                messages.success(request, 'Success')
                return redirect('adminGroupDetail', pk=pk)
            else:
                messages.error(request, 'Error occurred while saving group')
                post_data['id'] = pk
                post_data = user_service.getPostData(post_data, None)
                return render(request, 'admin/groups/add_group.html',
                              {'postData': post_data, 'permissions': permissions})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            print(post_form.errors)
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = user_service.getPostData(post_data, errors)
            return render(request, 'admin/groups/add_group.html',
                          {'postData': post_data, 'permissions': permissions})
