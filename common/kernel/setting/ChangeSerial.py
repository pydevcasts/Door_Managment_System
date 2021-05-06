from Lang import CHANGE_SERIAL
from common.kernel.setting.Command import Command


class ChangeSerial(Command):
    def __init__(self):
        Command.__init__(self, 3095, CHANGE_SERIAL, "images/serial32.png")
