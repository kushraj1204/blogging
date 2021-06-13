from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone
import datetime
import pytz
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from Users.models import CustomUser
from datetime import date

from administrator.services.base import BaseService


class GroupService(BaseService):

    def getAll(self, keyword):
        users = CustomUser.objects.all().filter(
            Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(email__icontains=keyword) | Q(
                username__icontains=keyword) | Q(phone__icontains=keyword)).order_by('-id')

        return users

    def getById(self, id):
        user = get_object_or_404(CustomUser, pk=id)
        user.dob = date.isoformat(user.dob)
        return user


    def saveGroup(self, user_data, pk):
        try:
            if "dob" in user_data:
                date_format = '%Y-%m-%d'
                unaware_dob = datetime.datetime.strptime(user_data['dob'], date_format)
                aware_dob = pytz.utc.localize(unaware_dob)
                user_data['dob'] = aware_dob
        except Exception as e:
            print(e)
            print('datetimeerror')
            pass
        if pk:
            try:
                if "password" in user_data:
                    user_data['password'] = make_password(user_data['password'])
            except Exception as e:
                print(e)
                pass
            try:
                update_data = user_data
                status = CustomUser.objects.filter(pk=pk).update(**update_data)
                if status:
                    return {'id': pk, 'success': True}
            except Exception as e:
                print(e)
                pass

        else:
            try:
                if "id" in user_data:
                    user_data.pop('id')
                user = CustomUser(**user_data)
                user.password = make_password(user.password)
                status = user.save()
                if status:
                    return {'id': user.pk, 'success': True}
            except Exception as e:
                print(e)
                pass
        return {'id': pk if pk else 0, 'success': False}