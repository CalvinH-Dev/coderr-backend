import os

from django.db.models.fields.files import FieldFile


def extract_filename(field_file: FieldFile) -> str:
    """Extracts only the filename from a Django FieldFile object."""
    return os.path.basename(field_file.name)
