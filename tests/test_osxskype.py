from unittest import TestCase
from skype.osx import OSXSkype


class TestOSXSkype(TestCase):

    def test_launch(self):
        s = OSXSkype()
        print s.launch()

    def test_hangup(self):
        s = OSXSkype()
        s.hangup()

    def test_call_ids(self):
        s = OSXSkype()
        print s._get_call_ids()

    def test_dial(self):
        s = OSXSkype()
        s.launch()
        s.dial('+18666824770')

    def test_hide(self):
        s = OSXSkype()
        s.hide()
