class AppleScriptError(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        super(AppleScriptError, self).__init__("%d: %s\n%s\n%s" % (returncode, stdout, stderr, script))

class SkypeError(Exception):
    pass
