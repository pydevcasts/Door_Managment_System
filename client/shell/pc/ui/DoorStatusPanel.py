from Globals import interface
from PyQtImports import pyqtSignal
from client.shell.pc.PasswordManager import passwordManager
from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.CStatusButton import CStatusButton


class DoorStatusPanel(CRowPanel):
    updateUiSignal = pyqtSignal()

    #######################################################################################
    def __init__(self):
        CRowPanel.__init__(self)
        self.statusButtons = []
        self.updateUiSignal.connect(self.updateUiSlot)

    #######################################################################################
    def updateUiSlot(self):
        statusList = interface.get().getDoorStatusList()
        for status in statusList:
            button = CStatusButton(status, self.statusButtonClicked)
            self.statusButtons.append(button)
            self.addSingle(button)

        interface.get().addStatusListener(doorStatusPanel)

    #######################################################################################
    def versionFound(self, model, version):
        self.updateUiSignal.emit()

    #######################################################################################
    def selectionAccepted(self):
        interface.get().setSettingMode(False)
        return True

    #######################################################################################
    def statusButtonClicked(self, baseStatus):
        if not interface.get().isSerialConnected():
            return

        if not passwordManager.userAccess():
            return

        from common.kernel.request.SetStatusRequest import SetStatusRequest
        request = SetStatusRequest(baseStatus.key)

        passwordManager.fillRequest(request)

        interface.get().handle(request)

    #######################################################################################
    def statusChanged(self, status):
        for button in self.statusButtons:
            if button.baseStatus.key == status:
                button.select()
            else:
                button.unselect()


######################################################################
######################################################################
######################################################################
doorStatusPanel = DoorStatusPanel()
