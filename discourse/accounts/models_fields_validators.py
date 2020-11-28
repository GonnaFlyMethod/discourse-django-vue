from django.core.exceptions import ValidationError


def image_size_limit(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        msg = 'File too large. Size should not exceed 2 MB.'
        raise ValidationError(msg)