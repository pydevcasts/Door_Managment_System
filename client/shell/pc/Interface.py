import sys


class Interface:

    ############################################################################
    def __init__(self):

        self.initialCheck()

        self.kernel = None

        from PyQtImports import QApplication
        self.app = QApplication(sys.argv)

        from Globals import logger
        from client.shell.pc.LogManager import logManager
        logger.addLogListener(logManager)

    ############################################################################
    def initialCheck(self):
        try:
            from PyQtImports import Qt
        except:
            print("'PyQt' is not installed. Execute: 'sudo apt-get install python-Qt4'")
            sys.exit()

    ############################################################################
    def start(self):

        # from common.shell.AppIcon import appIcon
        # self.app.setWindowIcon(appIcon)

        from common.shell.ui.UI import universalStyle
        self.app.setStyleSheet(universalStyle())

        # Check Liscence
        # from Globals import ini
        # from client.shell.pc.ui.ValidationDialog import validationDialog
        # validationDialog.show(ini.getLsc())
        # ini.setLsc(validationDialog.lsc)

        """
        # create and show splash
        from client.shell.pc.ui.CSplash import splash
        splash.show()

        # Wait enough seconds to dispay splash
        import time
        start = time.time()
        while time.time() < start + 2:
            app.processEvents()
        """

        from client.shell.pc.ui.ConfigPanel import configPanel
        self.kernel.addConfigurationsTo(configPanel)

        # create and show main window
        from client.shell.pc.ui.MainWindow import mainWindow
        mainWindow.show()

        # splash.finish(Globals.mainWindow)

        # start password manager
        from client.shell.pc.PasswordManager import passwordManager
        passwordManager.start()

        sys.exit(self.app.exec_())

    ############################################################################
    def initKernel(self, kernel):
        self.kernel = kernel

        from client.shell.pc.ui.DoorStatusPanel import doorStatusPanel
        self.kernel.addVersionListener(doorStatusPanel)

        from client.shell.pc.setting.SettingsManager import settingsManager
        self.kernel.addVersionListener(settingsManager)
        self.kernel.addSettingListener(settingsManager)

    ############################################################################
    def handle(self, request):
        return self.kernel.handle(request)

    ############################################################################
    def setSettingMode(self, mode):
        self.kernel.setSettingMode(mode)

    ############################################################################
    def isSerialConnected(self):
        return self.kernel.isSerialConnected()

    #################################################################################
    def addStatusListener(self, listener):
        return self.kernel.addStatusListener(listener)

    ############################################################################
    def getDoorStatusList(self):
        return self.kernel.getDoorStatusList()

    ############################################################################
    def getSettings(self):
        return self.kernel.getSettings()

    #################################################################################
    def addConfiguration(self, title, getter, setter):
        from client.shell.pc.ui.ConfigPanel import configPanel
        configPanel.addConfig(title, getter, setter)

    #################################################################################
    def addDoorErrorListener(self, listener):
        self.kernel.addDoorErrorListener(listener)
