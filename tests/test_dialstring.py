from unittest import TestCase
from skype.dial import DialString


class TestDialString(TestCase):

    def test_basic(self):
        d = DialString('tel:+18555123456,mp1234*#')
        self.assertEqual(d.number, '+18555123456')
        self.assertEqual(d.dtmf, 'mp1234*#')

        d = DialString('tel:+18555123456,mp1234*#')
        self.assertEqual(d.number, '+18555123456')
        self.assertEqual(d.dtmf, 'mp1234*#')
