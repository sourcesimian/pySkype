import re
from time import sleep


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


def dial(tel, dtmf_pause=10, dtmf_delay=2):
    d = DialString(tel)
    from skype.osx import OSXSkype
    skype = OSXSkype()

    skype.hangup()
    try:
        print "dialing: %s" % d.number
        skype.dial(d.number)
        if d.dtmf:
            wait_for(dtmf_pause)
            print "dtmf: %s" % d.dtmf

            def mute():
                print "mute: ON"
                skype.mute()

            char_map = {
                ',': lambda: sleep(dtmf_delay),
                'p': lambda: wait_for('pause'),
                'm': lambda: mute(),
            }
            for char in d.dtmf:
                if char in char_map:
                    char_map[char]()
                else:
                    skype.send_tone(char)
                    sleep(0.4)
    except KeyboardInterrupt:
        skype.hangup()


def wait_for(arg):
    if isinstance(arg, (int, float)):
        print "waiting: %fs" % arg
        sleep(arg)
    else:
        raw_input("waiting: \"%s\". Press ENTER ..." % arg)

