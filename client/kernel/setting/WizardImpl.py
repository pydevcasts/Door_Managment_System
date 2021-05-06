from client.kernel.setting.CommandImpl import CommandImpl
from common.kernel.setting.Wizard import Wizard


class WizardImpl(CommandImpl):

    ################################################################################
    def __init__(self):
        CommandImpl.__init__(self)
        self.state = Wizard.STATE_CLOSE
        self.buffer = None

    ################################################################################
    def execute(self, request):
        raise Exception("execute won't be called for wizards. try another methods.")

    ################################################################################
    def getState(self):
        return self.state

    ################################################################################
    def getBufferedState(self):
        if self.buffer is None:
            return self.getState()

        buffer = self.buffer
        self.clearBuffer()
        return buffer

    ################################################################################
    def setState_(self, state):
        self.state = state
        return True

    ################################################################################
    def setState(self, state):
        return self.setState_(state)

    ################################################################################
    def bufferState(self, state):
        self.buffer = state

    ################################################################################
    def clearBuffer(self):
        self.buffer = None

    ################################################################################
    def start(self):
        return self.setState_(Wizard.STATE_START)

    ################################################################################
    def cancel(self):
        return self.setState_(Wizard.STATE_CANCEL)
