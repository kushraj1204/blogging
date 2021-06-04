from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages

from Users.models import CustomUser
from administrator.services.auth import AuthService


class BaseAdminView(View):
    loggedInUser = None

    def dispatch(self, request, *args, **kwargs):

        if request.session.get('loggedInUser') is None:
            return redirect('adminLogin')
        else:
            id = request.session.get('loggedInUser')['id']
            user = vars(CustomUser.objects.get(pk=id))
            auth_service = AuthService()
            return_data = auth_service.affirm_user_access(user)
            if not return_data['data']:
                messages.error(request, return_data['message'])
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)
