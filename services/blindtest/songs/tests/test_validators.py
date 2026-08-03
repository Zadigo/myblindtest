from datetime import datetime

import pytest
from django.core.exceptions import ValidationError

from songs.validators import (
    validate_difficulty,
    validate_year,
    validate_youtube,
)


@pytest.mark.parametrize(
    "value",
    [
        2020,
        datetime.now().year + 1,
    ]
)
def test_validate_year(value):
    if value > datetime.now().year:
        with pytest.raises(ValidationError):
            validate_year(value)
    else:
        validate_year(value)
        


@pytest.mark.parametrize(
    "value",
    [
        "https://www.youtube.com/embed/abc123",
        "http://example.com"
    ]
)
def test_validate_youtube(value):
    if value == "http://example.com":
        with pytest.raises(ValidationError):
            validate_youtube(value)
    else:
        validate_youtube(value)


@pytest.mark.parametrize(
    "value",
    [
        0,
        1,
        3,
        5,
        6
    ]
)
def test_validate_difficulty(value):
    if value not in [1, 3, 5]:
        with pytest.raises(ValidationError):
            validate_difficulty(value)
    else:
        validate_difficulty(value)



def test_validate_wikipedia_page():
    pass
