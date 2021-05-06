from PyQtImports import QWidget, QGridLayout, QFrame, QScrollArea
from server.setting.WrapperFactory import wrapperFactory


class SettingsPanel(QWidget):

    ############################################################################
    def __init__(self, doorPanel):
        QWidget.__init__(self)
        self.doorPanel = doorPanel

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

        self.currentPanel = None

        settings = self.getSettings()
        self.settingsPackWrapper = wrapperFactory.wrap(settings, doorPanel=self.doorPanel)
        self.settingsPackWrapper.activate(self)

    ############################################################################
    def addWidget(self, panel):
        if self.currentPanel is not None:
            self.gridLayout.removeWidget(self.currentPanel)
            self.currentPanel.setParent(None)

        self.currentPanel = panel
        if panel is not None:
            self.gridLayout.addWidget(panel, 0, 0)

    ############################################################################
    def getSettings(self):
        # Simple Settings
        return self.doorPanel.struct.getSettings()[0]

    ############################################################################
    def updateOn(self, doorI):
        if doorI is None or not hasattr(doorI, "params"):
            return

        for parameterCode, value in doorI.params.items():
            wrappers = self.settingsPackWrapper.findAll(parameterCode)
            for wrapper in wrappers:
                wrapper.setValue(value)

    #############################################################################
    def setSettingValue(self, parameterCode, value):

        wrappers = self.settingsPackWrapper.findAll(parameterCode)
        for wrapper in wrappers:
            wrapper.setValue(value)


################################################################################
################################################################################
class AdvancedSettingsPanel(SettingsPanel):

    ############################################################################
    def __init__(self, doorPanel):
        SettingsPanel.__init__(self, doorPanel)

    ############################################################################
    def getSettings(self):
        # Advanced Settings
        return self.doorPanel.struct.getSettings()[1]
