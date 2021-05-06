import threading
import time

from PyQtImports import QWidget, QGridLayout
from PyQtImports import pyqtSignal
from common.kernel.Structure import structure
from common.kernel.core.Role import *
from common.kernel.request.InfoResponse import InfoResponse
from common.shell.ui.CTitleAndLogo import CTitleAndLogo
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog
from server.core.DoorList import doorList
from server.ui.door.DoorTabbedPane import DoorTabbedPane
from server.ui.door.ErrorsPanel import ErrorsPanel
from server.ui.door.MechanicalPanel import MechanicalPanel
from server.ui.door.PasswordsPanel import PasswordsPanel
from server.ui.door.SettingsPanel import SettingsPanel, AdvancedSettingsPanel
from server.ui.door.StatusPanel import StatusPanel


class DoorPanel(QWidget):
    updateSignal = pyqtSignal()

    #############################################################################
    def __init__(self, serial, role, alertMethod=None):
        QWidget.__init__(self)

        self.serial = serial
        self.role = role
        self.alertMethod = alertMethod

        self.connectionStatus = None

        door = self.getDoor()
        self.struct = structure.get(door.model, door.version)

        self.currentPanel = None
        self.doorTabbedPane = None
        self.statusPanel = None
        self.passwordsPanel = None
        self.settingsPanel = None
        self.advancedSettingsPanel = None
        self.errorsPanel = None
        self.mechanicalPanel = None

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(25)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 0)
        self.layout.setColumnStretch(0, 1)

        self.updateSignal.connect(self.updateSlot)

        self.title = CTitleAndLogo()
        self.title.setText(door.name)
        self.layout.addWidget(self.title, 0, 0, 1, 1)

        self.updateSignal.emit()

        doorList.addListener(self)

        self.active = True
        self.reloadDoorThread = threading.Thread(target=self.reloadDoor)
        self.reloadDoorThread.setDaemon(True)
        self.reloadDoorThread.start()

    #############################################################################
    def getDoor(self):
        door = doorList.findDoor(self.serial)
        return door

    #############################################################################
    def createDigitalView(self, role):

        self.closePanel()

        if self.statusPanel is None:

            self.statusPanel = StatusPanel(self)

            # only one item
            if role >= ROLE_ADVANCED_USER:

                self.doorTabbedPane = DoorTabbedPane()
                statusItem = self.doorTabbedPane.addItem("Door Status", "images/door.png", self.onDoorStatusClicked)
                statusItem.select()

                self.passwordsPanel = PasswordsPanel(self, role)
                self.doorTabbedPane.addItem("Passwords", "images/passwords.png", self.onPasswordsClicked)

                if role >= ROLE_OWNER:
                    self.settingsPanel = SettingsPanel(self)
                    self.doorTabbedPane.addItem("Settings", "images/settings.png", self.onSettingsClicked)

                if role >= ROLE_INSTALLER:
                    self.advancedSettingsPanel = AdvancedSettingsPanel(self)
                    self.doorTabbedPane.addItem("Advanced Settings", "images/advancedsettings.png", self.onAdvancedSettingsClicked)

                if role >= ROLE_OWNER:
                    self.errorsPanel = ErrorsPanel(self, role)
                    self.doorTabbedPane.addItem("Errors", "images/errors.png", self.onErrorsClicked)

                if role >= ROLE_OWNER:
                    self.doorTabbedPane.addItem("Enable Mechanical", "images/mechanical.png", self.onMechanicalClicked, False)

                self.doorTabbedPane.addItem("Enable SSK", "images/ssk.png", self.onSskClicked, False)

        self.layout.addWidget(self.doorTabbedPane, 2, 0, 1, 1)
        self.onDoorStatusClicked()

    #############################################################################
    def createMechanicalView(self, role):
        self.closePanel()
        self.closePanel(self.doorTabbedPane)

        if self.mechanicalPanel is None:
            self.mechanicalPanel = MechanicalPanel(self, role)

        self.addPanel(self.mechanicalPanel)

    #############################################################################
    def addPanel(self, panel):
        if panel is None:
            return

        if panel == self.currentPanel:
            return

        self.closePanel()

        self.layout.addWidget(panel, 1, 0, 1, 1)
        self.currentPanel = panel

    #############################################################################
    def closePanel(self, panel=None):

        if panel is None:
            panel = self.currentPanel
            self.currentPanel = None

        if panel is not None:
            self.layout.removeWidget(panel)
            panel.setParent(None)

    #############################################################################
    def onDoorStatusClicked(self):
        self.addPanel(self.statusPanel)

    #############################################################################
    def onPasswordsClicked(self):
        self.addPanel(self.passwordsPanel)

    #############################################################################
    def onSettingsClicked(self):
        self.addPanel(self.settingsPanel)

    #############################################################################
    def onAdvancedSettingsClicked(self):
        self.addPanel(self.advancedSettingsPanel)

    #############################################################################
    def onSskClicked(self):
        door = self.getDoor()
        dialog = CQuestionDialog("Enable SSK for " + door.name + "?")
        if not dialog.show():
            return

        from common.kernel.request.SskRequest import SskRequest
        request = SskRequest()
        response, exception = self.callRequest(request)

        if exception is not None:
            self.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.error()
            return

        if response.isBuffered():
            # TODO a waiting mechanism
            self.alert("It might take a few seconds")
            return

        self.alert("SSK enabled successfully.")

    #############################################################################
    def onMechanicalClicked(self):
        dialog = CQuestionDialog("Switch to mechanical state?")
        if not dialog.show():
            return

        from common.kernel.request.EnableMechanicalRequest import EnableMechanicalRequest
        request = EnableMechanicalRequest(True)
        response, exception = self.callRequest(request)

        if exception is not None:
            self.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.error()
            return

        if response.isBuffered():
            # TODO a waiting mechanism
            self.alert("It might take a few seconds")
            return

        self.alert("Mechanical state enabled successfully.")

    #############################################################################
    def onErrorsClicked(self):
        self.errorsPanel.refresh()
        self.addPanel(self.errorsPanel)

    #############################################################################
    def doorListChanged(self):
        self.updateSignal.emit()

    #############################################################################
    def updateSlot(self):

        door = self.getDoor()
        if door is None or not door.isConnectionValid():
            self.close()
            return

        if door.connectionStatus != self.connectionStatus:
            self.connectionStatus = door.connectionStatus
            if door.isDigital():
                self.createDigitalView(self.role)
            elif door.isMechanical():
                self.createMechanicalView(self.role)

        self.title.setText(door.name)

        if door.isMechanical():
            return

        if self.statusPanel is not None:
            self.statusPanel.updateOn(door)

        if self.settingsPanel is not None:
            self.settingsPanel.updateOn(door)

        if self.advancedSettingsPanel is not None:
            self.advancedSettingsPanel.updateOn(door)

        if self.errorsPanel is not None:
            self.errorsPanel.updateOn(door)

    #############################################################################
    def reloadDoor(self):

        from common.kernel.request.DoorRequest import DoorRequest
        request = DoorRequest()

        maxErrors = 2
        errorCounter = maxErrors

        while self.active:
            time.sleep(5)
            if not self.active:
                break

            from server.exception.DmsException import DmsException
            try:
                doorResponse, _ = self.callRequest(request)
                if doorResponse is not None and doorResponse.isSuccessful():
                    doorList.insert(doorResponse)
                    errorCounter = maxErrors
                    continue

            except DmsException:
                pass

            if errorCounter <= 0:
                break
            errorCounter -= 1

        doorList.changeConnectionStatus(self.serial, InfoResponse.CONNECTION_STATUS_INVALID)

    #############################################################################
    def callRequest(self, request):
        from server.connection.ConnectionManager import connectionManager
        try:
            response = connectionManager.get().callRequest(request, self.getDoor())
            return response, None
        except Exception as e:
            return None, e

    #############################################################################
    def close(self):
        doorList.removeListener(self)
        self.active = False
        door = self.getDoor()
        if door is not None:
            door.password = None

    #############################################################################
    def setSettingValue(self, parameterCode, value):
        if self.settingsPanel is not None:
            self.settingsPanel.setSettingValue(parameterCode, value)
        if self.advancedSettingsPanel is not None:
            self.advancedSettingsPanel.setSettingValue(parameterCode, value)

    #############################################################################
    def error(self, text="Error!"):
        self.alert(text, True)

    #############################################################################
    def alert(self, text, error=False):

        if self.alertMethod is not None:
            return self.alertMethod(text, error)

        from common.shell.ui.dialog.CAlertDialog import CAlertDialog
        CAlertDialog(str(text)).show()
