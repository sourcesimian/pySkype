from skype.dial import dial


def skype():
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument('tel', help='e.g. "tel:+18001234567,123456#,1234#p#"')
    arg_parser.add_argument('--dtmf-pause', default=10, help='seconds to wait after dialing')
    arg_parser.add_argument('--dtmf-delay', default=2, help='seconds at a comma')

    args = arg_parser.parse_args()

    dial(args.tel, args.dtmf_pause, args.dtmf_delay)

