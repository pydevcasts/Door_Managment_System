import sys

from PyQtImports import QApplication


class Interface:

    ############################################################################
    def __init__(self):
        self.kernel = None
        self.app = QApplication(sys.argv)

        # from Globals import logger
        # from client.shell.pc.LogManager import logManager
        # logger.addLogListener(logManager)

        self.simpleSettings = None
        self.advancedSettings = None

    ############################################################################
    def start(self):
        from common.shell.AppIcon import appIcon
        self.app.setWindowIcon(appIcon)

        from common.shell.ui.UI import universalStyle
        self.app.setStyleSheet(universalStyle())

        # create and show main window
        from client.shell.admin.ui.MainWindow import mainWindow
        mainWindow.show()

        sys.exit(self.app.exec_())

    ############################################################################
    def initKernel(self, kernel):
        self.kernel = kernel
        self.kernel.addVersionListener(self)
        self.kernel.setSettingMode(True)

    ################################################################################
    def versionFound(self, version, model):
        self.simpleSettings, self.advancedSettings = self.kernel.getSettings()

    ############################################################################
    def handle(self, request):
        return self.kernel.handle(request)

    ############################################################################
    # def setSettingMode(self, mode):
    #    self.kernel.setSettingMode(mode)

    ############################################################################
    def isSerialConnected(self):
        return self.kernel.isSerialConnected()

    ############################################################################
    def getSettings(self):
        return self.simpleSettings, self.advancedSettings

    #################################################################################
    # def addConfiguration(self, title, getter, setter):
    #    from client.shell.pc.ui.ConfigPanel import configPanel
    #    configPanel.addConfig(title, getter, setter)
