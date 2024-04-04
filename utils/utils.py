import os
import uuid

from django.conf import settings


def get_post_photo_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return '{}/{}{}'.format(settings.POST_PHOTOS, uuid.uuid4(), extension)
