import os
import time, datetime
import traceback
import string
import random

from django.conf import settings
from django.http import HttpResponse
import json

from administrator.views.base import BaseAdminView


class Images(BaseAdminView):

    def post(self, request):
        try:
            uploaded_filename = request.FILES['file'].name
            split_up = os.path.splitext(uploaded_filename)
            ext = split_up[-1]
            rand_filename = self.random_string_generator()
            unique_filename = rand_filename + str(int(time.time())) + ext
            subfolder = '\\images\\userimages\\' + str(datetime.date.today()) + '\\'
            if not os.path.exists(settings.MEDIA_ROOT + subfolder):
                os.makedirs(settings.MEDIA_ROOT + subfolder)
            saved_path = subfolder + unique_filename
            full_filename = os.path.join(settings.MEDIA_ROOT + saved_path)
            for key, file in request.FILES.items():
                dest = open(full_filename, 'wb')
                if file.multiple_chunks:
                    for c in file.chunks():
                        dest.write(c)
                else:
                    dest.write(file.read())
                dest.close()
            return HttpResponse(json.dumps({'result': True,
                                            'data': {'filename': uploaded_filename, 'saved_filename': saved_path,
                                                     'message': None}}), content_type="application/json")
        except:
            print(traceback.format_exc())
            return HttpResponse(
                json.dumps({'result': False, 'message': 'There was an error in uploading file', 'data': None}),
                content_type="application/json")

    def random_string_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
