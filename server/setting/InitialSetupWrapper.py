import time

from common.kernel.request.WizardRequest import WizardRequest
from common.kernel.setting.InitialSetup import InitialSetup
from common.kernel.setting.Wizard import Wizard
from common.shell.ui.dialog.InitialSetupDialog import InitialSetupDialog
from server.setting.CommandWrapper import CommandWrapper


class InitialSetupWrapper(CommandWrapper):

    ################################################################################
    def __init__(self, command, doorPanel):
        CommandWrapper.__init__(self, command, doorPanel)

    ################################################################################
    def execute(self):
        """ PyQT"""
        dialog = InitialSetupDialog(self.onStart, self.onCancel, self.onScan)
        dialog.show()

    ################################################################################
    def callRequest(self, state):
        request = WizardRequest(self.command.parameterCode, state)
        return self.doorPanel.callRequest(request)

    ################################################################################
    def onStart(self):
        response, exception = self.callRequest(Wizard.STATE_START)
        return response is not None and response.isSuccessful()

    ################################################################################
    def onCancel(self):
        response, exception = self.callRequest(Wizard.STATE_CANCEL)
        return response is not None and response.isSuccessful()

    ################################################################################
    def onScan(self):
        response, exception = self.callRequest(InitialSetup.STATE_SCAN_START)
        if response is None or not response.isSuccessful():
            return False

        while True:

            time.sleep(1)

            response, exception = self.callRequest(Wizard.STATE_IGNORE)
            if response is None or not response.isSuccessful():
                return False

            state = response.state

            if state == Wizard.STATE_FAIL:
                return False

            if state == Wizard.STATE_CANCEL:
                return False

            if state == Wizard.STATE_SUCCESS:
                return True
