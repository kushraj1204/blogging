from django.shortcuts import redirect, render, get_object_or_404

from administrator.forms.settings import SettingsForm
from administrator.services.users import UserService
from administrator.views.base import BaseAdminView
from django.contrib import messages
from ..models import Settings
import json


class SettingsView(BaseAdminView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs, session_menu='Settings', session_submenu='',
                                permission_required=[])

    def get(self,request):
        user_service = UserService()
        settings = get_object_or_404(Settings, pk=1)
        post_data = user_service.getPostData(vars(settings), None)
        return render(request, 'admin/settings/index.html',
                      {'postData': post_data})

    def post(self, request):
        pk=1
        _post_data = request.POST
        post_data = _post_data.dict()
        post_data.pop('csrfmiddlewaretoken')
        user_service = UserService()
        settings = get_object_or_404(Settings, pk=pk)
        post_form = SettingsForm(post_data, instance=settings)
        if post_form.is_valid():
            status = post_form.save()
            if status:
                messages.success(request, 'Success')
                return redirect('adminSettings')
            else:
                messages.error(request, 'Error occurred while saving settings')
                post_data = user_service.getPostData(post_data, None)
                return render(request, 'admin/settings/index.html',
                              {'postData': post_data,})

        else:
            messages.error(request, 'Form validation Error. Please correct the below mentioned errors')
            errors = json.loads(post_form.errors.as_json())  # errors to json and then to dict
            post_data = user_service.getPostData(post_data, errors)
            return render(request, 'admin/settings/index.html',
                          {'postData': post_data,})
