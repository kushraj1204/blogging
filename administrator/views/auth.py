from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from administrator.services.auth import AuthService
from administrator.views.base import BaseAdminView
from django.views.generic import View
import json


class Login(View):

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('loggedInUser') is not None:
            return redirect('adminHome')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'admin/pages/login.html', {})

    def post(self, request):
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")
        auth_service = AuthService()
        exists = auth_service.login(username, password)
        if exists['data']:
            request.session['loggedInUser'] = exists['data']
            messages.success(request, 'Login Success')
            return redirect('adminHome')
        else:
            messages.error(request, exists['message'])
        return render(request, 'admin/pages/login.html', {'postData': {'username': username, 'password': password}})


class Logout(BaseAdminView):

    def post(self, request):
        request.session.flush()
        return HttpResponse(json.dumps({'data': 'success'}), content_type="application/json")
