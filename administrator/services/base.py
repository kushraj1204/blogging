from Users.models import CustomUser


class BaseService:

    def affirm_user_access(self, exists):
        session_data = {}
        if not exists['is_superuser']:  # superuser doesnt need any special permissions to do anything
            if not exists['is_staff']:
                return {'data': False, 'message': 'Staff status has not been activated yet'}
            if not exists['is_active']:
                return {'data': False, 'message': 'User account is not activated yet'}
        session_data['full_name'] = exists['first_name'] + ' ' + exists['last_name']
        session_data['id'] = exists['id']
        session_data['profile_image'] = exists['profile_image']
        return {'data': session_data, 'message': 'Username and password matched'}

    def getPostData(self, post_data, errors):
        return_data = dict()
        for datakey, eachdata in post_data.items():
            return_data[datakey] = dict()
            field_dict = dict()
            field_dict['value'] = eachdata if eachdata is not None else ""
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
