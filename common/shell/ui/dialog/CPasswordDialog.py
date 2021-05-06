from Lang import ENTER_PASSWORD
from PyQtImports import QIntValidator
from PyQtImports import QLineEdit
from common.shell.ui.dialog.CTextInputDialog import CTextInputDialog


class CPasswordDialog(CTextInputDialog):

    #############################################################################
    def __init__(self, label=ENTER_PASSWORD):
        CTextInputDialog.__init__(self, label)

        self.textBox.setEchoMode(QLineEdit.Password)

        validator = QIntValidator()
        self.textBox.setValidator(validator)

    #############################################################################
    def show(self):
        self.textBox.clear()
        CTextInputDialog.show(self)

    #############################################################################
    def getPassword(self):
        return self.getText()
