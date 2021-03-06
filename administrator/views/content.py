from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from administrator.forms.content import ContentForm
from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
import json

from blogs.models import Content


class ContentView(BaseAdminView):

    @classmethod
    def get_list(cls, request):
        response = cls.pre_function(cls, request, session_menu='Content', session_submenu='',
                                    permissions_required=['blogs.view_content'])
        if not response['status']:
            return response['action']
        keyword = request.GET.get('keyword')
        filter = {'keyword': keyword if keyword is not None else ""}
        if keyword is None:
            keyword = ''
        contents = Content.objects.all().filter(
            Q(title__icontains=keyword)).order_by('id')
        paginator = Paginator(contents, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/content/index.html',
                      {'paginator': paginator, 'page_number': page_number, 'page_obj': page_obj,
                       'filter': filter})

    @classmethod
    def add(cls, request):
        response = cls.pre_function(cls, request, session_menu='Content', session_submenu='',
                                    permissions_required=['blogs.add_content'])
        if not response['status']:
            return response['action']
        if request.method == 'POST':
            _post_data = request.POST
            post_data = _post_data.dict()
            post_data.pop('csrfmiddlewaretoken')
            user_service = UserService()
            content = Content()
            post_form = ContentForm(post_data, instance=content)
            if post_form.is_valid():
                status = post_form.save()
                if status:
                    cls.log_to_admin(cls, modelname='content', object_id=content.pk, object_repr=post_data['title'],
                                     action_flag=1,
                                     change_message=json.dumps([{'added': {}}]))
                    messages.success(request, 'Success')
                    return redirect('adminContentDetail', pk=content.pk)
                else:
                    messages.error(request, 'Error occurred while saving content')
                    post_data['id'] = 0
                    post_data = user_service.getPostData(post_data, None)
                    return render(request, 'admin/content/add_content.html',
                                  {'postData': post_data, })

            else:
                messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
                print(post_form.errors)
                errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
                post_data = user_service.getPostData(post_data, errors)
                return render(request, 'admin/content/add_content.html',
                              {'postData': post_data, })

        else:
            content = Content()
            content.id = 0
            user_service = UserService()
            post_data = user_service.getPostData(vars(content), None)
            return render(request, 'admin/content/add_content.html',
                          {'postData': post_data})

    @classmethod
    def delete(cls, request, pk):
        response = cls.pre_function(cls, request, session_menu='Content', session_submenu='',
                                    permissions_required=['blogs.delete_content'])
        if not response['status']:
            messages.error(request, 'You are unauthorized to complete this action')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

        _post_data = request.POST
        try:
            content = get_object_or_404(Content, pk=pk)
            status = content.delete()
        except:
            status = 0
        if status:
            cls.log_to_admin(cls, modelname='content', object_id=pk, object_repr=content.__str__(), action_flag=3,
                             change_message=json.dumps([{'deleted': {}}]))
            messages.success(request, 'Content Deleted Successfully')
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            messages.error(request, 'There was a problem in deleting the content')
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")

    def get(self, request, pk):
        if not pk:
            return redirect('adminContentAdd')
        response = self.pre_function(request, session_menu='Content', session_submenu='',
                                     permissions_required=['blogs.view_content'])
        if not response['status']:
            return response['action']
        user_service = UserService()
        content = get_object_or_404(Content, pk=pk)
        post_data = user_service.getPostData(vars(content), None)

        return render(request, 'admin/content/add_content.html',
                      {'postData': post_data, })

    def post(self, request, pk):
        response = self.pre_function(request, session_menu='Content', session_submenu='',
                                     permissions_required=['blogs.change_content'])
        if not response['status']:
            return response['action']
        _post_data = request.POST
        post_data = _post_data.dict()
        post_data.pop('csrfmiddlewaretoken')
        user_service = UserService()
        content = get_object_or_404(Content, pk=pk)
        post_form = ContentForm(post_data, instance=content)
        if post_form.is_valid():
            status = post_form.save()
            if status:
                changed_fields = self.getChangedFields(post_data, content)
                if len(changed_fields) > 0:
                    self.log_to_admin(modelname='content', object_id=pk, object_repr=content.__str__(), action_flag=2,
                                      change_message=json.dumps([{'changed': {'fields': changed_fields}}]))

                messages.success(request, 'Success')
                return redirect('adminContentDetail', pk=pk)
            else:
                messages.error(request, 'Error occurred while saving content')
                post_data['id'] = pk
                post_data = user_service.getPostData(post_data, None)
                return render(request, 'admin/content/add_content.html',
                              {'postData': post_data, })

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            print(post_form.errors)
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = user_service.getPostData(post_data, errors)
            return render(request, 'admin/content/add_content.html',
                          {'postData': post_data, })
