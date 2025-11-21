from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'{value} is not a valid year. It cannot be in the future.')


def validate_difficulty(value):
    if value < 1 or value > 5:
        raise ValidationError(
            "Difficulty should be a between "
            "1 and 5"
        )
