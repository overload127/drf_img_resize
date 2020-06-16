from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

import os


def validate_image_size(image):
    """
    Validator for files, checking the size
    """
    file_size = image.size
    limit_mb = 10
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'Max size of file is {limit_mb} MB')


def validator_image_dpi(image):
    """
    Validator for files, checking the width, height
    """
    limit_height = limit_width = 10000
    width, height = get_image_dimensions(image)

    if height > limit_height:
        raise ValidationError(f'Max height of file is {limit_height} pixel')

    if width > limit_width:
        raise ValidationError(f'Max width of file is {limit_width} pixel')


def validate_image_extension(image):
    """
    Validator for files, checking the extension
    """
    ext = os.path.splitext(image.name)[1]
    type_content = image.image.format

    valid_extensions = [('.jpg', 'JPEG'), ('.png', 'PNG')]
    if not (ext.lower(), type_content) in valid_extensions:
        raise ValidationError(f'Unsupported file[{type_content}] extension[{ext}]. ')
