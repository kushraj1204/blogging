from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages

from Users.models import CustomUser
from administrator.services.auth import AuthService


class BaseAdminView(View):
    loggedInUser = None
    userpermissions = []
    groups = []

    def pre_function(self, request, session_menu='', session_submenu='', permissions_required=[], set_messages=True,
                     must_be_superuser=False):
        request.session['menu'] = session_menu
        request.session['submenu'] = session_submenu
        permissions_required = set(permissions_required)
        if request.session.get('loggedInUser') is None:
            return {'status': False, 'message': 'logout', 'action': redirect('adminLogin')}
        else:
            self.loggedInUser = request.session.get('loggedInUser')
            id = self.loggedInUser['id']
            user = get_object_or_404(CustomUser, pk=id)
            permissions_access = user.get_all_permissions()
            groups = list(user.groups.all())
            group_ids = []
            for group in groups:
                group_ids.append(group.id)
            self.groups = group_ids
            self.userpermissions = permissions_access
            if not user.is_superuser:
                if must_be_superuser:
                    if set_messages:
                        messages.error(request, 'Not authorized')
                    return {'status': False, 'message': 'unauthorized', 'action': redirect('adminHome')}
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
