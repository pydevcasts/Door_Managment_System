from Globals import interface
from PyQtImports import QWidget, QGridLayout, QFrame, QScrollArea
from client.shell.pc.PasswordManager import passwordManager
from client.shell.pc.setting.SettingsManager import settingsManager


class SettingsPanel(QWidget):

    ########################################################################
    def __init__(self):
        QWidget.__init__(self)

        outerLayout = QGridLayout(self)
        outerLayout.setContentsMargins(2, 2, 2, 2)
        outerLayout.setSpacing(0)
        outerLayout.setRowStretch(0, 1)
        outerLayout.setColumnStretch(0, 1)

        self.mainWidget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(self.mainWidget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outerLayout.addWidget(scroll, 0, 0, 1, 1)

        self.gridLayout = QGridLayout(self.mainWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setColumnStretch(0, 1)

        self.widget = None

    ########################################################################
    def access(self):
        return passwordManager.ownerAccess()

    ########################################################################
    def selectionAccepted(self):

        if not interface.get().isSerialConnected():
            return

        if not self.activate():
            return False

        if not self.access():
            return False

        interface.get().setSettingMode(True)
        return True

    ########################################################################
    def activate(self):
        return settingsManager.activateSimple(self) > 0

    ########################################################################
    def addWidget(self, widget):
        if self.widget is not None:
            self.gridLayout.removeWidget(self.widget)
            self.widget.setParent(None)

        self.widget = widget
        if widget is not None:
            self.gridLayout.addWidget(widget, 0, 0)


########################################################################
########################################################################
########################################################################
settingsPanel = SettingsPanel()
