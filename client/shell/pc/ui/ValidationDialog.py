from PyQtImports import QLabel
from common.kernel.lsc.Validator import validator
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CStatusBarDialog import CStatusBarDialog


class ValidationDialog(CStatusBarDialog):

    ############################################################################
    def __init__(self):
        CStatusBarDialog.__init__(self)

        self.lsc = None

        from Lang import OK, CANCEL, HELP

        self.label = QLabel("Enter License key:")
        self.textBox = CLineEdit()
        self.textBox.setMinimumSize(250, 25)
        self.addDouble(self.label, self.textBox)

        self.okButton = self.addButton(OK)
        self.okButton.clicked.connect(self.okClicked)

        self.cancelButton = self.addButton(CANCEL)
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.helpButton = self.addButton(HELP)
        self.helpButton.clicked.connect(self.helpClicked)

        self.statusListenTo(self.textBox)

    ############################################################################
    def show(self, lsc):
        self.lsc = lsc
        if validator.validate(lsc):
            return
        CStatusBarDialog.show(self)

    ############################################################################
    def close(self):
        CStatusBarDialog.close(self)
        self.textBox.clear()

    ############################################################################
    def cancelClicked(self):
        from sys import exit
        exit()

    ############################################################################
    def okClicked(self):

        if self.textBox.text() is None or len(self.textBox.text()) == 0:
            self.setStatusText("No License key, please enter something")
            return

        self.lsc = self.textBox.text()

        if not validator.validate(self.lsc):
            self.setStatusText("Invalid License key!")
            return

        self.close()

    ############################################################################
    def helpClicked(self):
        self.close()
        from client.shell.pc.ui.ValidationHelpDialog import validationHelpDialog
        validationHelpDialog.show()


################################################################################
################################################################################
################################################################################

validationDialog = ValidationDialog()
