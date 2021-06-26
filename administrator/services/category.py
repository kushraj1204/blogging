from administrator.services.base import BaseService
from blogs.models import Category


class CategoryService(BaseService):

    def get_categories(self, new=False, getRoot=True):
        parents = list(Category.objects.filter(published=1).order_by('id', 'level').values('id', 'title', 'level'))
        if not getRoot:
            parents.pop(0)
        if new:
            parents.insert(0, {'id': 0, 'title': '---'})
        return parents
