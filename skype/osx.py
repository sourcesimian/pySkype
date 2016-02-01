import subprocess

from skype.exception import SkypeError, AppleScriptError


class OSXSkype(object):
    __call_id = None

    def launch(self):
        script = """\
            tell application "Skype"
                reopen
                activate
                set status to send command "GET USERSTATUS" script name "pySkype"
                return status
            end tell
        """
        status = self.__run_applescript(script)
        if status == 'COMMAND_PENDING':
            return False
        return True

    def hangup(self):
        for call_id in self._get_call_ids()[1:]:
            self._hangup(call_id)

    def hide(self):
        script = """\
            tell application "Finder"
                set visible of process "Skype" to false
            end tell
        """
        self.__run_applescript(script)

    def quit(self):
        script = """\
            tell application "Skype"
                quit
            end tell
        """
        self.__run_applescript(script)

    def _hangup(self, call_id):
        script = """\
            on SkypeHangup(call_id)
                tell application "Skype"
                    send command "ALTER CALL " & call_id & " HANGUP" script name "pySkype"
                end tell
            end SkypeHangup

            SkypeHangup(%(call_id)s)
            """ % {'call_id': call_id}
        self.__run_applescript(script)

    def _get_call_ids(self):
        script = """\
            on SkypeCallIds()
                tell application "Skype"
                    set calls to send command "SEARCH ACTIVECALLS" script name "pySkype"
                    return calls
                end tell
            end SkypeCallIds
            SkypeCallIds()
        """
        resp = self.__run_applescript(script)
        return resp.split()

    def dial(self, number):
        script = """\
            on SkypeDial(phone_number)
                tell application "Skype"
                    set active_call to send command "CALL " & phone_number script name "pySkype"
                    set skype_call_id to word 2 of active_call
                end tell
                return skype_call_id
            end SkypeDial

            SkypeDial("%(number)s")
            """ % {'number': number}
        self.__call_id = int(self.__run_applescript(script))

    def send_tone(self, tone):
        script = """\
            on SkypeDTMFTone(tone)
                set skype_call_id to (%(skype_call_id)s)
                tell application "Skype"
                    set bridge to "ALTER CALL " & skype_call_id & " DTMF "
                    send command bridge & " " & tone script name "pySkype"
                end tell
            end CallWithDTMF

            SkypeDTMFTone("%(tone)s")
            """ % {'tone': tone, 'skype_call_id': self.__call_id}
        self.__run_applescript(script)

    def mute(self, state=True):
        script = """\
            tell application "Skype"
                send command "SET MUTE %s" script name "pySkype"
            end tell
            """ % "ON "if state else "OFF"
        self.__run_applescript(script)

    def __run_applescript(self, script):
        from textwrap import dedent
        script = dedent(script)
        osa = subprocess.Popen(['osascript', '-'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
        stdout, stderr = osa.communicate(script)
        if osa.returncode != 0:
            raise AppleScriptError(osa.returncode, stdout, stderr, script)
        if stdout.startswith('ERROR'):
            raise SkypeError(stdout)
        return stdout
