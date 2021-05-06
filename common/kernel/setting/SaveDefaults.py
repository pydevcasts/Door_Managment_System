from Lang import SAVE_AS_DEFAULT
from common.kernel.setting.Command import Command


class SaveDefaults(Command):
    def __init__(self):
        Command.__init__(self, 3093, SAVE_AS_DEFAULT, "images/savedefault32.png")
