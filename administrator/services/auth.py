from django.contrib.auth.hashers import check_password
from django.db.models import Q
import datetime
from django.utils import timezone

from Users.models import CustomUser


class AuthService:

    def login(self, username, password):
        exists = CustomUser.objects.filter(
            Q(username=username) | Q(email=username) | Q(phone=username)
        ).values().first()
        if exists is not None:
            password_valid = check_password(password, exists['password'])
            if password_valid:
                CustomUser.objects.filter(pk=exists['id']).update(last_login=timezone.now())
                return_data = self.affirm_user_access(exists)
                return return_data

        return {'data': False, 'message': 'Incorrect username password combination'}

    def affirm_user_access(self, exists):
        if not exists['is_staff']:
            return {'data': False, 'message': 'Staff status has not been activated yet'}
        if not exists['is_active']:
            return {'data': False, 'message': 'User account is not activated yet'}
        exists['full_name'] = exists['first_name'] + ' ' + exists['last_name']
        exists['dob'] = str(exists['dob'])
        exists['last_login'] = str(exists['last_login'])
        exists['date_joined'] = str(exists['date_joined'])
        exists['lat'] = str(exists['lat'])
        exists['lng'] = str(exists['lng'])
        return {'data': exists, 'message': 'Username and password matched'}
