from Lang import lget, OK, CANCEL
from PyQtImports import QLabel
from common.shell.ui.dialog.CDialog import CDialog


class CQuestionDialog(CDialog):

    #############################################################################
    def __init__(self, question, okText=OK, onOkClicked=None, cancelText=CANCEL, onCancelClicked=None):
        CDialog.__init__(self)

        self.onOkClicked = onOkClicked
        self.onCancelClicked = onCancelClicked

        self.label = QLabel(lget(question))
        self.addSingle(self.label)

        self.okButton = self.addButton(okText)
        self.okButton.clicked.connect(self.okClicked)

        self.cancelButton = self.addButton(cancelText)
        self.cancelButton.clicked.connect(self.cancelClicked)

    ############################################################################
    def show(self):
        CDialog.show(self)
        return self.isAccepted()

    #############################################################################
    def okClicked(self):
        self._accepted = True
        if self.onOkClicked is not None:
            return self.onOkClicked()
        self.close()

    #############################################################################
    def cancelClicked(self):
        self._accepted = False
        if self.onCancelClicked is not None:
            return self.onCancelClicked()
        self.close()
