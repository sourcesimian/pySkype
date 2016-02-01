from time import sleep

from skype.dial import DialString
from skype.osx import OSXSkype


def skype():
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument('tel', help='e.g. "tel:+18001234567,123456#,1234#p#"')
    arg_parser.add_argument('--dtmf-pause', default=10, help='seconds to wait after dialing')
    arg_parser.add_argument('--dtmf-delay', default=2, help='seconds at a comma')

    args = arg_parser.parse_args()

    actions = {
        'h': hangup,
        'launch': launch,
        'hide': hide,
        'quit': quit,
    }

    if args.tel in actions:
        actions[args.tel]()
        return
    dial(args.tel, args.dtmf_pause, args.dtmf_delay)


def hangup():
    s = OSXSkype()
    s.hangup()


def launch():
    s = OSXSkype()
    s.launch()


def hide():
    s = OSXSkype()
    s.hide()


def quit():
    s = OSXSkype()
    s.hide()


def dial(tel, dtmf_pause=10, dtmf_delay=2):
    d = DialString(tel)
    from skype.osx import OSXSkype
    skype = OSXSkype()

    if not skype.launch():
        print "Please allow pySkype to use Skype"
        exit(1)
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

            def hangup():
                print "hangup"
                skype.hangup()

            char_map = {
                ',': lambda: sleep(dtmf_delay),
                'p': lambda: wait_for('pause'),
                'm': lambda: mute(),
                'h': lambda: hangup(),
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


