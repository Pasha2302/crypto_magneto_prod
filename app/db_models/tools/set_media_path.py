import os
from datetime import datetime
from django.utils.text import slugify


def build_media_path(instance, filename, folder: str, is_default=False):
    ext = filename.split(".")[-1].lower()
    if not is_default:
        slug = getattr(instance, "slug", "file")
    else :
        slug = 'file'

    model_name = instance.__class__.__name__.lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slugify(slug)}-{timestamp}.{ext}"

    if slug == 'file':
        path = os.path.join(model_name, folder, filename)
    else:
        path = os.path.join(model_name, folder, slug, filename)

    return path


def default_image_upload_path(instance, filename):
    return build_media_path(instance, filename, folder="images", is_default=True)


def image_upload_path(instance, filename):
    return build_media_path(instance, filename, folder="images")


def video_upload_path(instance, filename):
    return build_media_path(instance, filename, folder="videos")
