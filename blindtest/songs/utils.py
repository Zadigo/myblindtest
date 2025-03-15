import random
from base64 import b32encode
import datetime
import pyotp
import qrcode
from django.conf import settings
from django.utils import timezone


def create_token():
    number_value = random.randint(1000, 9999)
    date_value = timezone.now().timestamp()
    return f"game_{number_value}_{int(date_value)}"


class OTPCode:
    """Class used to create an OTP code
    that can be used to sign into a blind
    test session"""

    def __init__(self):
        secret_key = b32encode(bytearray(settings.SECRET_KEY, 'ascii'))
        self.instance = pyotp.TOTP(secret_key.decode('utf-8'))
        self.url = self.instance.provisioning_uri(
            name='Blind Test', issuer_name='Django')

    @property
    def get_qr_code(self):
        return qrcode.make(self.url)

    def get_code(self):
        return self.instance.now()

    def verify(self, code):
        return self.instance.verify(code)


def astrologic_sign(date_of_birth: datetime.datetime | None, translate=False) -> str | None:
    if date_of_birth is None:
        return None

    dates = {
        'Bélier': [
            datetime.datetime(year=date_of_birth.year, month=3, day=20),
            datetime.datetime(year=date_of_birth.year, month=4, day=19)
        ],
        'Taureau': [
            datetime.datetime(year=date_of_birth.year, month=4, day=20),
            datetime.datetime(year=date_of_birth.year, month=5, day=20)
        ],
        'Gémeaux': [
            datetime.datetime(year=date_of_birth.year, month=5, day=21),
            datetime.datetime(year=date_of_birth.year, month=6, day=21)
        ],
        'Cancer': [
            datetime.datetime(year=date_of_birth.year, month=6, day=22),
            datetime.datetime(year=date_of_birth.year, month=7, day=22)
        ],
        'Lion': [
            datetime.datetime(year=date_of_birth.year, month=7, day=23),
            datetime.datetime(year=date_of_birth.year, month=8, day=22)
        ],
        'Vierge': [
            datetime.datetime(year=date_of_birth.year, month=8, day=23),
            datetime.datetime(year=date_of_birth.year, month=9, day=22)
        ],
        'Balance': [
            datetime.datetime(year=date_of_birth.year, month=9, day=23),
            datetime.datetime(year=date_of_birth.year, month=10, day=23)
        ],
        'Scorpion': [
            datetime.datetime(year=date_of_birth.year, month=10, day=24),
            datetime.datetime(year=date_of_birth.year, month=11, day=22)
        ],
        'Sagittaire': [
            datetime.datetime(year=date_of_birth.year, month=11, day=23),
            datetime.datetime(year=date_of_birth.year, month=12, day=22)
        ],
        'Capricorne': [
            datetime.datetime(year=date_of_birth.year, month=12, day=23),
            datetime.datetime(year=date_of_birth.year, month=1, day=20)
        ],
        'Verseau': [
            datetime.datetime(year=date_of_birth.year, month=1, day=21),
            datetime.datetime(year=date_of_birth.year, month=2, day=19)
        ],
        'Poissons': [
            datetime.datetime(year=date_of_birth.year, month=2, day=20),
            datetime.datetime(year=date_of_birth.year, month=3, day=20)
        ]
    }

    candidates = []
    for key, d in dates.items():
        start, end = d
        if date_of_birth >= start and date_of_birth <= end:
            candidates.append(key)

    sign = candidates[-1]
    if translate:
        translations = {
            'Bélier': 'Aries',
            'Taureau': 'Taurus',
            'Gémeaux': 'Gemini',
            'Cancer': 'Cancer',
            'Lion': 'Leo',
            'Vierge': 'Virgo',
            'Balance': 'Libra',
            'Scorpion': 'Scorpio',
            'Sagittaire': 'Sagittarius',
            'Capricorne': 'Capricorn',
            'Verseau': 'Aquarius',
            'Poissons': 'Pisces'
        }
        return translations.get(sign)
    return sign
