from administrator.services.base import BaseService
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime
import pytz
from Users.models import CustomUser
from blogs.models import Blog


class BlogService(BaseService):

    def saveBlog(self, blog_data, pk=0, loggedInuser=None):
        if pk:
            try:
                update_data = blog_data
                blog = Blog.objects.get(pk=pk)
                if not blog.alias:
                    update_data['alias'] = blog.generate_alias()
                status = Blog.objects.filter(pk=pk).update(**update_data)
                if status:
                    return {'id': pk, 'success': True}
            except Exception as e:
                print(e)
                pass

        else:
            try:
                update_data = blog_data
                update_data['cat_id_id'] = update_data['cat_id']
                update_data.pop('cat_id')
                blog = Blog(**update_data)
                print(blog)
                blog.alias = blog.generate_alias()
                status = blog.save()
                if status:
                    return {'id': blog.pk, 'success': True}
            except Exception as e:
                print(e)
                pass
        return {'id': pk if pk else 0, 'success': False}
