from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone
import datetime
import pytz
from django.shortcuts import get_object_or_404
from Users.models import CustomUser
from datetime import date

from administrator.email import EmailThread
from administrator.services.base import BaseService


class UserService(BaseService):

    def getAll(self, keyword):

        users = CustomUser.objects.all().filter(
            Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(email__icontains=keyword) | Q(
                username__icontains=keyword) | Q(phone__icontains=keyword)).order_by('-id')

        return users

    def getById(self, id):
        user = get_object_or_404(CustomUser, pk=id)
        user.dob = date.isoformat(user.dob)
        return user

    def saveUser(self, user_data, pk):
        try:
            if "dob" in user_data:
                if not user_data['dob']:
                    user_data['dob'] = timezone.now()
                else:
                    date_format = '%Y-%m-%d'
                    unaware_dob = datetime.datetime.strptime(user_data['dob'], date_format)
                    aware_dob = pytz.utc.localize(unaware_dob)
                    user_data['dob'] = aware_dob
        except Exception as e:
            user_data['dob'] = timezone.now()
            pass
        if pk:
            update_groups = False
            update_user_permissions = False
            if "groups" in user_data:
                groups = user_data['groups']
                update_groups = True
                user_data.pop('groups')
            if "user_permissions" in user_data:
                user_permissions = user_data['user_permissions']
                update_user_permissions = True
                user_data.pop('user_permissions')
            if "password" in user_data:
                user_data['password'] = make_password(user_data['password'])
            try:
                update_data = user_data
                status = CustomUser.objects.filter(pk=pk).update(**update_data)
                if status:
                    saved_user = CustomUser.objects.get(pk=pk)
                    if update_groups:
                        saved_user.groups.clear()
                        saved_user.groups.add(*groups)
                    if update_user_permissions:
                        saved_user.user_permissions.clear()
                        saved_user.user_permissions.add(*user_permissions)
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
                    self.send_activation_email(user)

                    return {'id': user.pk, 'success': True}
            except Exception as e:
                print(e)
                pass
        return {'id': pk if pk else 0, 'success': False}

    def send_activation_email(self, user):
        #any formattings here
        EmailThread(subject="Account activation email", message="Click here to activate your email",
                    email_from="info@kushblogs.com",
                    email_to=[user.email]).start()
