import os

from django.utils.text import slugify


def profile_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    username = slugify(instance.user.username)
    return f"profile_images/{username}_picture{ext}"
