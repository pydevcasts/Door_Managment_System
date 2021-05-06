from Lang import LOAD_DEFAULTS
from common.kernel.setting.Command import Command


class LoadDefaults(Command):
    def __init__(self):
        Command.__init__(self, 3094, LOAD_DEFAULTS, "images/loaddefault32.png")