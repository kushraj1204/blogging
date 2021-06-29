from django.shortcuts import redirect, render

from administrator.views.base import BaseAdminView


class Dashboard(BaseAdminView):

    def get(self, request):
        response=self.pre_function(request, session_menu='Home', session_submenu='', permissions_required=[])
        if not response['status']:
            return response['action']
        return render(request, 'admin/pages/dashboard.html', {'hello': 'World'})
