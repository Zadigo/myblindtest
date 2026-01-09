import datetime

from django.test import TestCase
from songs import utils
from songs.utils import OTPCode

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


class TestUtils(TestCase):
    def test_otp_util(self):
        instance = OTPCode()
        code = instance.get_code()
        self.assertIsNotNone(code)
        self.assertTrue(instance.verify(code))

    def test_astrologic_sign_util(self):
        d = datetime.datetime(year=2000, month=10, day=1)
        sign = utils.astrologic_sign(d.date())
        self.assertEqual(sign, 'Balance')

        # There seems to be a problem when trying to
        # get data for january artists
        dates = [
            (datetime.datetime(year=1996, month=1, day=15).date(), 'Capricorne'),
            (datetime.datetime(year=1996, month=2, day=15).date(), 'Verseau'),
            (datetime.datetime(year=1996, month=3, day=18).date(), 'Poissons')
        ]

        for item, expected in dates:
            with self.subTest(item=item):
                sign = utils.astrologic_sign(item)
                self.assertEqual(sign, expected)
