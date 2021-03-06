import os
import time, datetime
import traceback
import string
import random
from PIL import Image
from django.conf import settings
from django.http import HttpResponse
import json

from administrator.email import EmailThread
from administrator.views.base import BaseAdminView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


class Images(BaseAdminView):

    def post(self, request):
        imagetype = request.POST.get('imagetype')
        if imagetype not in ["userimages", "common_media", "blogimages"]:
            return HttpResponse(
                json.dumps({'result': False, 'message': 'There was an error in uploading file', 'data': None}),
                content_type="application/json")
        try:
            f = request.FILES['file']
            f.seek(0, 2)
            file_length = (f.tell()) / (1024 * 1024)
            if file_length > 5:
                return HttpResponse(
                    json.dumps(
                        {'result': False, 'message': 'File too large. Select at most of 5 MB file', 'data': None}),
                    content_type="application/json")
            uploaded_filename = f.name
            split_up = os.path.splitext(uploaded_filename)
            ext = split_up[-1]
            rand_filename = self.random_string_generator()
            unique_filename = rand_filename + str(int(time.time())) + ext
            subfolder = '\\images\\' + imagetype + '\\'
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

            self.generate_sizes(subfolder, unique_filename, thumbonly=True if imagetype == 'common_media' else False)
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
                # response.append("common_media/" + f)
                response.append(str(f))
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

    @staticmethod
    def generate_sizes(subfolder, unique_filename, thumbonly=False):
        # here ill use predefined dimension sizes for ease
        saved_path = subfolder + unique_filename
        full_filename = os.path.join(settings.MEDIA_ROOT + saved_path)
        if not thumbonly:
            subfolderlarge = subfolder + 'large\\'
            subfoldermedium = subfolder + 'medium\\'
            if not os.path.exists(settings.MEDIA_ROOT + subfolderlarge):
                os.makedirs(settings.MEDIA_ROOT + subfolderlarge)
            if not os.path.exists(settings.MEDIA_ROOT + subfoldermedium):
                os.makedirs(settings.MEDIA_ROOT + subfoldermedium)
        subfolderthumb = subfolder + 'thumb\\'
        if not os.path.exists(settings.MEDIA_ROOT + subfolderthumb):
            os.makedirs(settings.MEDIA_ROOT + subfolderthumb)

        sizes = [{'path': subfolderthumb, 'maxsize': 100}]
        if not thumbonly:
            sizes.append({'path': subfolderlarge, 'maxsize': 800})
            sizes.append({'path': subfoldermedium, 'maxsize': 400})
        try:
            img = Image.open(full_filename)
            width, height = img.size
            aspect_ratio = width / height
            for size in sizes:
                newimg = img
                if width > size['maxsize'] or height > size['maxsize']:
                    if width >= height:
                        newheight = size['maxsize']
                        newwidth = newheight * aspect_ratio
                    else:
                        newwidth = size['maxsize']
                        newheight = newwidth / aspect_ratio
                    if (newwidth * newheight) < (width * height):  # we dont want a bigger size after compressing
                        newimg = img.resize((round(newwidth), round(newheight)))
                newimg.save(os.path.join(settings.MEDIA_ROOT + size['path'] + unique_filename))
        except Exception as e:
            print(e)
