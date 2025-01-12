import random
from base64 import b32encode

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

    @ property
    def get_qr_code(self):
        return qrcode.make(self.url)

    def get_code(self):
        return self.instance.now()

    def verify(self, code):
        return self.instance.verify(code)
