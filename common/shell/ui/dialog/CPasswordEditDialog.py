from PyQtImports import QLabel, QLineEdit
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CStatusBarDialog import CStatusBarDialog


class CPasswordEditDialog(CStatusBarDialog):

    ###########################################################################################
    def __init__(self):
        CStatusBarDialog.__init__(self)

        from Lang import lget, OK, CANCEL, OLD_PASSWORD, NEW_PASSWORD, RETYPE_PASSWORD

        #  Old Password
        self.oldPasswordLabel = QLabel(lget(OLD_PASSWORD))

        self.oldPasswordTextBox = CLineEdit()
        self.oldPasswordTextBox.setMinimumSize(250, 25)
        self.oldPasswordTextBox.setEchoMode(QLineEdit.Password)
        self.addDouble(self.oldPasswordLabel, self.oldPasswordTextBox)

        #  New Password
        self.newPasswordLabel = QLabel(lget(NEW_PASSWORD))

        self.newPasswordTextBox = CLineEdit()
        self.newPasswordTextBox.setMinimumSize(250, 25)
        self.newPasswordTextBox.setEchoMode(QLineEdit.Password)
        self.addDouble(self.newPasswordLabel, self.newPasswordTextBox)

        #  New Password, again
        self.againPasswordLabel = QLabel(lget(RETYPE_PASSWORD))

        self.againPasswordTextBox = CLineEdit()
        self.againPasswordTextBox.setMinimumSize(250, 25)
        self.againPasswordTextBox.setEchoMode(QLineEdit.Password)
        self.addDouble(self.againPasswordLabel, self.againPasswordTextBox)

        #  buttons

        self.okButton = self.addButton(OK)
        self.okButton.clicked.connect(self.okClicked)

        self.cancelButton = self.addButton(CANCEL)
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.statusListenTo(self.oldPasswordTextBox)
        self.statusListenTo(self.newPasswordTextBox)
        self.statusListenTo(self.againPasswordTextBox)

    ###########################################################################################
    def getOldPassword(self):
        return str(self.oldPasswordTextBox.text())

    ###########################################################################################
    def getNewPassword(self):
        return str(self.newPasswordTextBox.text())

    ###########################################################################################
    def getAgainPassword(self):
        return str(self.againPasswordTextBox.text())

    ###########################################################################################
    def show(self):
        self._accepted = False
        CStatusBarDialog.show(self)

    ###########################################################################################
    def cancelClicked(self):
        self.close(False)

    ###########################################################################################
    def validate(self):

        from Lang import FILL_EMPTY_FIELDS, PASSWORDS_NOT_EQUAL

        oldPassword = self.getOldPassword()
        newPassword = self.getNewPassword()
        againPassword = self.getAgainPassword()

        if oldPassword is None or len(oldPassword) == 0:
            self.setStatusText(FILL_EMPTY_FIELDS)
            return False

        if newPassword is None or len(newPassword) == 0:
            self.setStatusText(FILL_EMPTY_FIELDS)
            return False

        if againPassword is None or len(againPassword) == 0:
            self.setStatusText(FILL_EMPTY_FIELDS)
            return False

        if newPassword != againPassword:
            self.setStatusText(PASSWORDS_NOT_EQUAL)
            return False

        return True

    ###########################################################################################
    def okClicked(self):

        if not self.validate():
            return

        self.close(True)
