import os.path
from django.conf import settings


def getImages(imagepath):
    returnimage = {}
    defaultimage = os.path.join('\\default.png')
    returnimage['large'] = defaultimage
    returnimage['medium'] = defaultimage
    returnimage['thumb'] = defaultimage
    if not imagepath:
        return returnimage
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT + imagepath)):
        filename = imagepath.split('\\')[-1]
        filebase = '\\'.join(imagepath.split('\\')[0:-1])
        if os.path.exists(settings.MEDIA_ROOT + filebase + '\\large\\'):
            largeimage = filebase + '\\large\\' + filename;
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT + largeimage)):
                returnimage['large'] = os.path.join(largeimage)
        if os.path.exists(settings.MEDIA_ROOT + filebase + '\\medium\\'):
            mediumimage = filebase + '\\medium\\' + filename;
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT + mediumimage)):
                returnimage['medium'] = os.path.join(mediumimage)
        if os.path.exists(settings.MEDIA_ROOT + filebase + '\\thumb\\'):
            thumbimage = filebase + '\\thumb\\' + filename;
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT + thumbimage)):
                returnimage['thumb'] = os.path.join(thumbimage)

    return returnimage
