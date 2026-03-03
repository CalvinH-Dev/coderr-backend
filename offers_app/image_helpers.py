import os

from django.utils.text import slugify


def offers_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    id = slugify(instance.id)
    return f"offer_images/offer_{id}_picture{ext}"
