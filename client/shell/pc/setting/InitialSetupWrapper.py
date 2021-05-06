import time

from Globals import interface
from client.shell.pc.PasswordManager import passwordManager
from client.shell.pc.setting.CommandWrapper import CommandWrapper
from common.kernel.request.WizardRequest import WizardRequest
from common.kernel.setting.InitialSetup import InitialSetup
from common.kernel.setting.Wizard import Wizard
from common.shell.ui.dialog.InitialSetupDialog import InitialSetupDialog


class InitialSetupWrapper(CommandWrapper):

    ################################################################################
    def __init__(self, initialSetup):
        CommandWrapper.__init__(self, initialSetup)

    ################################################################################
    def clicked(self):
        dialog = InitialSetupDialog(self.onStart, self.onCancel, self.onScan)
        dialog.show()

    ####################################################################################################
    def callRequest(self, state=Wizard.STATE_IGNORE):
        request = WizardRequest(3020, state)
        passwordManager.fillRequest(request)
        response = interface.get().handle(request)
        return response

    ################################################################################
    def onStart(self):
        response = self.callRequest(Wizard.STATE_START)
        return response is not None and response.isSuccessful()

    ################################################################################
    def onCancel(self):
        response = self.callRequest(Wizard.STATE_CANCEL)
        return response is not None and response.isSuccessful()

    ################################################################################
    def onScan(self):

        response = self.callRequest(InitialSetup.STATE_SCAN_START)
        if response is None or not response.isSuccessful():
            return False

        while True:

            time.sleep(0.5)

            response = self.callRequest(Wizard.STATE_IGNORE)
            if response is None or not response.isSuccessful():
                return False

            state = response.state

            if state == Wizard.STATE_FAIL:
                return False

            if state == Wizard.STATE_CANCEL:
                return False

            if state == Wizard.STATE_SUCCESS:
                return True

