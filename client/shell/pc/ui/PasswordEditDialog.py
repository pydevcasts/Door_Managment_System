from Globals import logger
from client.kernel.core.Authorizer import authorizer
from client.shell.pc.PasswordManager import passwordManager
from common.shell.ui.dialog.CPasswordEditDialog import CPasswordEditDialog


class PasswordEditDialog(CPasswordEditDialog):

    ###########################################################################################
    def __init__(self, role):
        CPasswordEditDialog.__init__(self)

        self.role = role
        self.title = authorizer.getText(role)

    ###########################################################################################
    def show(self):
        CPasswordEditDialog.show(self)

    ###########################################################################################
    def close(self, **kwargs):
        CPasswordEditDialog.close(self, **kwargs)
        self.oldPasswordTextBox.clear()
        self.newPasswordTextBox.clear()
        self.againPasswordTextBox.clear()

    ###########################################################################################
    def okClicked(self):

        if not self.validate():
            return

        oldPassword = self.getOldPassword()
        newPassword = self.getNewPassword()

        from common.kernel.request.SetPasswordRequest import SetPasswordRequest
        request = SetPasswordRequest(self.role, oldPassword, newPassword)

        passwordManager.fillRequest(request, oldPassword)

        from Globals import interface
        response = interface.get().handle(request)

        from Lang import ERROR

        if not response.isSuccessful():
            self.setStatusText(ERROR)
            return

        self._accepted = True

        from Lang import NEW_ROLE_PASSWORD_ACCEPTED
        logger.success(NEW_ROLE_PASSWORD_ACCEPTED, self.title)

        self.close()
