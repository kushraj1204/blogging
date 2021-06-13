from django.contrib.auth.hashers import check_password
from django.db.models import Q
import datetime
from django.utils import timezone

from Users.models import CustomUser
from administrator.services.base import BaseService


class AuthService(BaseService):

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

