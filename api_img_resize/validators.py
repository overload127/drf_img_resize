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
    max_height = max_width = 9999
    min_height = min_width = 1
    width, height = get_image_dimensions(image)

    if height > max_height:
        raise ValidationError(f'Max height of file is {max_height} pixel')

    if width > max_width:
        raise ValidationError(f'Max width of file is {max_width} pixel')

    if height < min_height:
        raise ValidationError(f'Min height of file is {min_height} pixel')

    if width < min_width:
        raise ValidationError(f'Min width of file is {min_width} pixel')


def validate_image_extension(image):
    """
    Validator for files, checking the extension
    """
    ext = os.path.splitext(image.name)[1]
    type_content = image.image.format

    valid_extensions = [('.jpg', 'JPEG'), ('.png', 'PNG')]
    if not (ext.lower(), type_content) in valid_extensions:
        raise ValidationError(
            f'Unsupported file[{type_content}] extension[{ext}]. ')


def validate_number_value(value):
    """
    Validator for height and width, checking the value
    """
    max_value = 9999
    min_value = 1

    if value > max_value:
        raise ValidationError(f'Max value of param is {max_value} pixel')

    if value < min_value:
        raise ValidationError(f'Min value of param is {min_value} pixel')
