from common.kernel.setting.Command import Command


class Wizard(Command):

    STATE_IGNORE = -3
    STATE_CANCEL = -2
    STATE_CLOSE = -1
    STATE_START = 0
    STATE_SUCCESS = 100
    STATE_FAIL = 200

    ################################################################################
    def __init__(self, parameterCode, title, imageAddress):
        Command.__init__(self, parameterCode, title, imageAddress)
