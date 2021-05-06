from Lang import OK, CANCEL
from PyQtImports import QLabel
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CStatusBarDialog import CStatusBarDialog


class SerialDialog(CStatusBarDialog):

    ##################################################################
    def __init__(self):
        CStatusBarDialog.__init__(self)

        label = QLabel("Enter Serial Number (8 characters between 0 and 9)                                      ")
        self.addSingle(label)

        self.ok = False

        self.serialText = CLineEdit()
        self.addSingle(self.serialText)
        self.statusListenTo(self.serialText)

        okButton = self.addButton(OK)
        okButton.clicked.connect(self.okClicked)

        cancelButton = self.addButton(CANCEL)
        cancelButton.clicked.connect(self.cancelClicked)

        generateButton = self.addButton("Generate")
        generateButton.clicked.connect(self.generateClicked)

    ##################################################################
    def validate(self):
        serialNo = self.getSerial()

        if serialNo is None or len(serialNo) != 8:
            self.setStatusText("The serial number must contain exactly 8 characters.")
            return False

        for i in range(0, 8):
            if ord(serialNo[i]) < ord('0') or ord(serialNo[i]) > ord('9'):
                self.setStatusText("You've used '" + serialNo[i] + "', but you should only use numbers between 0 and 9.")
                return False

        self.setStatusText("")
        return True

    ##################################################################
    def okClicked(self):
        if not self.validate():
            return
        self.ok = True
        self.close()

    ##################################################################
    def cancelClicked(self):
        self.ok = False
        self.close()

    ##################################################################
    def generateClicked(self):
        pass

    ##################################################################
    def getSerial(self):
        return str(self.serialText.text())
