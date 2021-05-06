from PyQtImports import QLabel
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CDialog import CDialog


class ValidationHelpDialog(CDialog):

    #############################################################################
    def __init__(self):
        CDialog.__init__(self)

        label = QLabel()
        label.setText("Give the following Identification key to your vendor and ask for a Liscense key:")
        self.addSingle(label)

        text = CLineEdit()
        from common.kernel.lsc.Hardware import getIdentificationCode
        text.setText(getIdentificationCode())
        text.setReadOnly(True)
        self.addSingle(text)

        okButton = self.addButton("OK")
        okButton.clicked.connect(self.okClicked)

    #############################################################################
    def okClicked(self):
        self.close()
        from sys import exit
        exit()

#################################################################################
#################################################################################
#################################################################################

validationHelpDialog = ValidationHelpDialog()
