from Lang import OK, lget
from PyQtImports import QLabel
from common.shell.ui.dialog.CDialog import CDialog


class CAlertDialog(CDialog):

    ############################################################################
    def __init__(self, text, *params):
        CDialog.__init__(self)

        self.label = QLabel(lget(str(text), *params))
        # self.label.setMinimumSize(250, 25)

        self.addSingle(self.label)

        self.okButton = self.addButton(OK)
        self.okButton.clicked.connect(self.close)
