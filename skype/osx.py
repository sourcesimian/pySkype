import subprocess


class OSXSkype(object):
    def hangup(self):
        script = """\
            on SkypeHangup()
                tell application "Skype"
                    set calls to send command "SEARCH ACTIVECALLS" script name "Call Control"
                    set callID to last word of calls
                    send command "ALTER CALL " & callID & " HANGUP" script name "Call Control"
                end tell
            end SkypeHangup

            SkypeHangup()
            """
        self.__run_applescript(script)

    def dial(self, number):
        script = """\
            on SkypeDial(phone_number)
                tell application "Skype"
                    set active_call to send command "CALL " & phone_number script name ""
                    set skype_call_id to word 2 of active_call
                end tell
                return skype_call_id
            end CallWithDTMF

            SkypeDial("%(number)s")
            """ % {'number': number}
        self.__call_id = int(self.__run_applescript(script))

    def send_tone(self, tone):
        script = """\
            on SkypeDTMFTone(tone)
                set skype_call_id to (%(skype_call_id)s)
                tell application "Skype"
                    set bridge to "ALTER CALL " & skype_call_id & " DTMF "
                    send command bridge & " " & tone script name "s2"
                end tell
            end CallWithDTMF

            SkypeDTMFTone("%(tone)s")
            """ % {'tone': tone, 'skype_call_id': self.__call_id}
        self.__run_applescript(script)

    def mute(self, state=True):
        script = """\
            tell application "Skype"
                send command "SET MUTE %s" script name "foo"
            end tell
            """ % "ON "if state else "OFF"
        self.__run_applescript(script)

    def __run_applescript(self, script):
        osa = subprocess.Popen(['osascript', '-'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
        return osa.communicate(script)[0]
