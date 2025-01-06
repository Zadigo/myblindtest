from base64 import b32encode
from urllib.parse import urlparse, urlunparse

import pyotp
import qrcode
from django.conf import settings
from django.utils.crypto import get_random_string


def create_token():
    token = get_random_string(length=5)
    return f'tok_{token}'


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


def clean_embed_url(url):
    parsed_url = urlparse(url)
    clean_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            None,
            None,
            None
        )
    )
    return clean_url
