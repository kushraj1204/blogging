from django.contrib.auth.hashers import make_password
from django.db.models import Q
from Users.models import CustomUser
from datetime import date


class UserService():

    def getAll(self, keyword):
        users = CustomUser.objects.all().filter(
            Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(email__icontains=keyword) | Q(
                username__icontains=keyword) | Q(phone__icontains=keyword)).order_by('-id')

        return users

    def getById(self, id):
        user = CustomUser.objects.get(pk=id)
        user.dob = date.isoformat(user.dob)
        return user

    def saveUser(self, user_data, pk):
        try:
            if user_data['dob']:
                user_data['dob'] = timezone(user_data['dob'])
        except:
            pass
        if pk:
            try:
                if user_data['password']:
                    user_data['password'] = make_password(user_data['password'])
            except:
                pass
            status = CustomUser.objects.filter(pk=pk).update(**user_data)
        else:
            user_data['id']=int(user_data['id'])
            user = CustomUser()

            user.fromdict(user_data)
            print('begin')
            print(user)
            print(user.lat)
            print(user.email)
            print('end')
            user.password = make_password(user.password)
            status = user.saveUser()
        return 1

    def getPostData(self, post_data, errors):
        return_data = dict()
        for datakey, eachdata in post_data.items():
            return_data[datakey] = dict()
            field_dict = dict()
            field_dict['value'] = eachdata
            field_dict['error'] = None
            if errors:
                for errorkey, eacherror in errors.items():
                    try:
                        if datakey == errorkey:
                            field_dict['error'] = eacherror[0]['message']
                    except:
                        pass
            return_data[datakey] = field_dict
        return return_data
