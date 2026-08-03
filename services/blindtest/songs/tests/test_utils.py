import datetime

import pytest
from django.test import TestCase

from songs import utils
from songs.utils import OTPCode

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

@pytest.mark.parametrize(
    "date, expected_sign",
    [
        (datetime.datetime(year=1996, month=1, day=15).date(), 'Capricorne'),
        (datetime.datetime(year=1996, month=2, day=15).date(), 'Verseau'),
        (datetime.datetime(year=1996, month=3, day=18).date(), 'Poissons'),
        (None, None)  # Test case for None input
    ]
)
def test_astrologic_sign_util(date: datetime.date, expected_sign: str):
    sign = utils.astrologic_sign(date)
    assert sign == expected_sign


@pytest.mark.parametrize(
    "month_name, expected_number",
    [
        ('Janvier', 1),
        ('janvier', 1),
        ('Février', 2),
        ('février', 2),
    ]
)
def test_month_to_number_util(month_name, expected_number):
    assert utils.month_to_number(month_name) == expected_number


@pytest.mark.parametrize(
    "month_number, expected_name",
    [
        (1, 'Janvier'),
        (2, 'Février'),
        (3, 'Mars'),
        (4, 'Avril'),
        (5, 'Mai'),
        (6, 'Juin'),
        (7, 'Juillet'),
        (8, 'Août'),
        (9, 'Septembre'),
        (10, 'Octobre'),
        (11, 'Novembre'),
        (12, 'Décembre'),
    ]
)
def test_month_to_text_util(month_number, expected_name):
    assert utils.month_to_text(month_number) == expected_name



def test_otp_util():
    instance = OTPCode()
    code = instance.get_code()
    
    assert code is not None
    assert instance.verify(code)

