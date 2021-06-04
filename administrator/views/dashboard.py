from django.shortcuts import redirect, render

from administrator.views.base import BaseAdminView


class Dashboard(BaseAdminView):

    def get(self, request):
        return render(request, 'admin/pages/dashboard.html', {'hello': 'World'})
