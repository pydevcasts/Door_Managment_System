from Globals import logger
from Lang import WAITING_FOR_PASSWORD, PLEASE_ENTER_A_PASSWORD, INVALID_PASSWORD, PASSWORD_ACCEPTED
from client.kernel.core.Authorizer import authorizer
from common.kernel.core.Role import ROLE_NONE
from common.shell.ui.dialog.CPasswordDialog import CPasswordDialog


class PasswordDialog(CPasswordDialog):

    #############################################################################
    def __init__(self):
        CPasswordDialog.__init__(self)

        self.role = ROLE_NONE
        self.password = None

    #############################################################################
    def show(self, role):
        self.role = role
        logger.info(WAITING_FOR_PASSWORD)
        CPasswordDialog.show(self)

    #############################################################################
    def okClicked(self):

        if self.isEmpty():
            self.setStatusText(PLEASE_ENTER_A_PASSWORD)
            return

        self.password = str(self.textBox.text())
        role = authorizer.getRole(self.password)
        self._accepted = role >= self.role

        if not self._accepted:
            logger.warning(INVALID_PASSWORD)
            self.setStatusText(INVALID_PASSWORD)
            return

        logger.success(PASSWORD_ACCEPTED)

        CPasswordDialog.okClicked(self)
