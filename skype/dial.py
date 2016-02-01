import re


class DialString(object):
    def __init__(self, s):
        if s.startswith('tel:'):
            s = s.split(':', 1)[1]
        number = s.split(',')[0]
        dtmf = s[len(number) + 1:]
        self.__number = re.sub(r'[^0-9+]', '', number)
        self.__dtmf = re.sub(r'[^0-9,pm*#]', '', dtmf)

    @property
    def number(self):
        return self.__number

    def __str__(self):
        return "tel:%s%s" % (self.__number, self.__dtmf)

    @property
    def dtmf(self):
        return self.__dtmf
