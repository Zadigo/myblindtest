import re
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_year(value):
    if value > 0:
        result = re.match(r'\d{4}', str(value))
        if not result:
            raise ValidationError('Year is not valid')

        current_date = timezone.now()
        if value > current_date.year:
            raise ValidationError('Year is not valid')


def validate_difficulty(value):
    if value < 1 or value > 5:
        raise ValidationError(
            "Difficulty should be a between "
            "1 and 5"
        )
