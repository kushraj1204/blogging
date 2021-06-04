import os
import time, datetime
import traceback

from django.conf import settings
from django.http import HttpResponse
import json

from administrator.views.base import BaseAdminView


class Images(BaseAdminView):

    def post(self, request):
        try:
            print(request.FILES.items)
            uploaded_filename = request.FILES['file'].name
            unique_filename = uploaded_filename + str(int(time.time()))
            subfolder = 'images\\userimages\\'
            print(settings.STATIC_ROOT+subfolder)
            if not os.path.exists(settings.STATIC_ROOT+subfolder):
                os.makedirs(settings.STATIC_ROOT+subfolder)
            saved_path = subfolder + str(datetime.date.today()) + "\\" + unique_filename
            full_filename = os.path.join(settings.STATIC_ROOT, saved_path)
            for key, file in request.FILES.items():
                path = file.name
                dest = open(path, 'w')
                if file.multiple_chunks:
                    for c in file.chunks():
                        dest.write(c)
                else:
                    dest.write(file.read())
                dest.close()
            # print(saved_path)
            # print(full_filename)
            # fout = open(full_filename, 'wb+')
            # for chunk in fout.chunks():
            #     fout.write(chunk)
            # fout.close()
            return HttpResponse(json.dumps({'result': True,
                                            'data': {'filename': uploaded_filename, 'saved_filename': saved_path,
                                                     'message': None}}), content_type="application/json")
        except:
            print(traceback.format_exc())
            return HttpResponse(
                json.dumps({'result': False, 'message': 'There was an error in uploading file', 'data': None}),
                content_type="application/json")
