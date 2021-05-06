from Lang import lget, OK, CANCEL
from PyQtImports import QLabel
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CStatusBarDialog import CStatusBarDialog


class CTextInputDialog(CStatusBarDialog):

    ############################################################################
    def __init__(self, label, placeHolder=None, defaultText=None):
        CStatusBarDialog.__init__(self)

        self.label = QLabel(lget(label))

        self.textBox = CLineEdit()
        self.textBox.setMinimumSize(250, 25)

        if placeHolder is not None:
            self.textBox.setPlaceholderText(lget(placeHolder))

        if defaultText is not None:
            self.textBox.setText(lget(defaultText))

        self.addDouble(self.label, self.textBox)

        self.okButton = self.addButton(OK)
        self.okButton.clicked.connect(self.okClicked)

        self.cancelButton = self.addButton(CANCEL)
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.statusListenTo(self.textBox)

    ############################################################################
    def isEmpty(self):
        return self.getText() is None or len(self.getText()) == 0

    ############################################################################
    def getText(self):
        if self.textBox.text() is None:
            return None
        return str(self.textBox.text())

    ############################################################################
    def show(self):
        self.statusBar.clear()
        CStatusBarDialog.show(self)

    ############################################################################
    def cancelClicked(self):
        self.close(False)

    ############################################################################
    def okClicked(self):
        self.close(True)
