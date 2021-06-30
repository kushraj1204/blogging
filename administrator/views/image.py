import os
import time, datetime
import traceback
import string
import random

from django.conf import settings
from django.http import HttpResponse
import json

from administrator.email import EmailThread
from administrator.views.base import BaseAdminView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


class Images(BaseAdminView):

    def post(self, request):
        EmailThread(subject="Subject", message="You just tried to upload an image didnt you", email_from="info@kushblogs.com",
                    email_to=["kushraj1204@gmail.com"]).start()


        imagetype = request.POST.get('imagetype')
        print(imagetype)
        if imagetype not in ["userimages", "common_media"]:
            return HttpResponse(
                json.dumps({'result': False, 'message': 'There was an error in uploading file', 'data': None}),
                content_type="application/json")
        try:
            uploaded_filename = request.FILES['file'].name
            split_up = os.path.splitext(uploaded_filename)
            ext = split_up[-1]
            rand_filename = self.random_string_generator()
            unique_filename = rand_filename + str(int(time.time())) + ext
            if imagetype == "userimages":
                subfolder = '\\images\\' + imagetype + '\\' + str(datetime.date.today()) + '\\'
            if imagetype == "common_media":
                subfolder = '\\' + imagetype + '\\'
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
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return HttpResponse(
                json.dumps({'result': False, 'message': 'There was an error in uploading file', 'data': None}),
                content_type="application/json")

    def random_string_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    def getImageList(cls, request):
        site = get_current_site(request)
        common_media = settings.MEDIA_ROOT + "//common_media"
        imgs = []
        response = []
        try:
            valid_images = [".jpg", ".png", ".jpeg"]
            for f in os.listdir(common_media):
                ext = os.path.splitext(f)[1]
                if ext.lower() not in valid_images:
                    continue
                each_image = {"src": os.path.join("http://" + str(site) + settings.MEDIA_URL + "common_media/" + f),
                              'title': f}
                response.append("common_media/" + f)
                imgs.append(each_image)
        except:
            pass
        # response = {'data': response}
        # return HttpResponse(
        #     json.dumps({'result': True, 'message': 'Image List', 'data': imgs}),
        #     content_type="application/json")
        return HttpResponse(
            json.dumps(response),
            content_type="application/json")
