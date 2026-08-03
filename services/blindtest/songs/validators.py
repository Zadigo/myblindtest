import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


def validate_year(value: int):
    if value > 0:
        result = re.match(r'\d{4}', str(value))
        if not result:
            raise ValidationError('Year is not valid')

        current_date = timezone.now()
        if value > current_date.year:
            raise ValidationError('Year is not valid')


def validate_youtube(value: str):
    validator = RegexValidator(r'youtube\.com\/embed\/')
    validator(value)


def validate_difficulty(value: int):
    if value < 1 or value > 5:
        raise ValidationError(
            "Difficulty should be a between "
            "1 and 5"
        )


def validate_wikipedia_page(value: str):
    if 'wikipedia.org/wiki/' not in value:
        raise ValidationError(
            'Url is not a valid Wikipediage page'
        )
