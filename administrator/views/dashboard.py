from django.shortcuts import redirect, render

from administrator.views.base import BaseAdminView


class Dashboard(BaseAdminView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs, session_menu='Home', session_submenu='',
                                permission_required=[])

    def get(self, request):
        return render(request, 'admin/pages/dashboard.html', {'hello': 'World'})
