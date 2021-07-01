from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages

from Users.models import CustomUser
from administrator.services.auth import AuthService

from administrator.utils import LoggingThread


class BaseAdminView(View):
    loggedInUser = None
    userpermissions = []

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
            self.userpermissions = permissions_access
            if not user.is_superuser:
                if must_be_superuser:
                    if set_messages:
                        messages.error(request, 'Access Forbidden')
                    return {'status': False, 'message': 'unauthorized', 'action': redirect('adminHome')}
                if not permissions_required.issubset(permissions_access):
                    if set_messages:
                        messages.error(request, 'Access Forbidden')
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

    def log_to_admin(self, modelname='logentry', object_id=1, object_repr='Object',
                     action_flag=2,
                     change_message='change'):
        LoggingThread(user_id=self.loggedInUser['id'], modelname=modelname, object_id=object_id,
                      object_repr=object_repr,
                      action_flag=action_flag,
                      change_message=change_message).start()

    @staticmethod
    def getChangedFields(post_data, object):
        object_list = vars(object)
        changed_fields = []
        for datakey, eachdata in post_data.items():
            if datakey in object_list:
                if type(post_data[datakey]) is bool:
                    post_data[datakey] = int(post_data[datakey] == 'True')
                if str(post_data[datakey]).strip() != str(object_list[datakey]).strip():
                    changed_fields.append(datakey)
        return changed_fields
