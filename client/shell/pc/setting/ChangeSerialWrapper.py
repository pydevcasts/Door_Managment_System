from PyQtImports import pyqtSignal
from client.shell.pc.setting.CommandWrapper import CommandWrapper
from common.shell.ui.CLineEdit import CLineEdit


class ChangeSerialWrapper(CommandWrapper):

    updateLabelTextSignal = pyqtSignal(object)

    ################################################################################
    def __init__(self, command):
        CommandWrapper.__init__(self, command)

    ################################################################################
    def createDialog(self):
        CommandWrapper.createDialog(self)
        self.lineEdit = CLineEdit()
        self.dialog.addSingle(self.lineEdit)


    ################################################################################
    def okClicked(self):
        self.lineEdit.setEnabled(False)
        CommandWrapper.okClicked(self)

    ################################################################################
    def createRequest(self):
        request = CommandWrapper.createRequest(self)
        request.addProperty("serial", str(self.lineEdit.text()))
        return request
