from django.test import TestCase

from songs.utils import OTPCode


class TestOTPCreation(TestCase):
    def test_general_structure(self):
        instance = OTPCode()
        code = instance.get_code()
        self.assertIsNotNone(code)
        self.assertTrue(instance.verify(code))
