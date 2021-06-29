from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages

from Users.models import CustomUser
from administrator.services.auth import AuthService


class BaseAdminView(View):
    loggedInUser = None
    userpermissions = []

    def pre_function(self, request, session_menu='', session_submenu='', permissions_required=[],set_messages=True):
        request.session['menu'] = session_menu
        request.session['submenu'] = session_submenu
        permissions_required = set(permissions_required)
        if request.session.get('loggedInUser') is None:
            return {'status': False, 'message': 'logout', 'action': redirect('adminLogin')}
        else:
            self.loggedInUser = request.session.get('loggedInUser')
            id = self.loggedInUser['id']
            user = CustomUser.objects.get(pk=id)
            permissions_access = user.get_all_permissions()
            self.userpermissions = permissions_access
            if not user.is_superuser:
                if not permissions_required.issubset(permissions_access):
                    if set_messages:
                        messages.error(request, 'Not authorized')
                    return {'status': False, 'message': 'unauthorized', 'action': redirect('adminHome')}
            user = vars(user)
            auth_service = AuthService()
            return_data = auth_service.affirm_user_access(user)
            if not return_data['data']:
                request.session.flush
                if set_messages:
                    messages.error(request, return_data['message'])
                return {'status': False, 'message': 'logout', 'action': redirect('adminLogin')}
            else:
                request.session['loggedInUser'] = return_data['data']
                request.session['permissions'] = list(permissions_access)
        return {'status': True, 'message': 'Success'}
