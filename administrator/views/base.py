from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages

from Users.models import CustomUser
from administrator.services.auth import AuthService


class BaseAdminView(View):
    loggedInUser = None

    def dispatch(self, request, *args, **kwargs):
        print('super dispatch')
        session_menu = kwargs['session_menu'] if "session_menu" in kwargs else ''
        session_submenu = kwargs['session_submenu'] if "session_submenu" in kwargs else ''
        request.session['menu'] = session_menu
        request.session['submenu'] = session_submenu
        print(session_menu)
        print('bho hai ta')

        permission_required = kwargs['permission_required'] if "permission_required" in kwargs else []
        permission_required = set(permission_required)

        if "session_menu" in kwargs:
            kwargs.pop('session_menu')
        if "session_submenu" in kwargs:
            kwargs.pop('session_submenu')
        if "permission_required" in kwargs:
            kwargs.pop('permission_required')

        if request.session.get('loggedInUser') is None:
            return redirect('adminLogin')

        else:
            self.loggedInUser = request.session.get('loggedInUser')
            id = self.loggedInUser['id']
            user = CustomUser.objects.get(pk=id)
            permissions_access = user.get_all_permissions()
            if not user.is_superuser:
                if not permission_required.issubset(permissions_access):
                    print('should redirect to unauthorized page ahile lai thikai chha')
                    pass
            user = vars(user)
            auth_service = AuthService()
            return_data = auth_service.affirm_user_access(user)
            if not return_data['data']:
                request.session.flush
                messages.error(request, return_data['message'])
                return redirect('adminLogin')
            else:
                request.session['loggedInUser'] = return_data['data']
                request.session['permissions'] = list(permissions_access)
        return super().dispatch(request, *args, **kwargs)
