#PYQT#from PyQtImports import QApplication

class Interface:

    ############################################################################
    def __init__(self):
        self.kernel = None
        #PYQT#self.app = QApplication(sys.argv)

        from Globals import logger
        logger.addLogListener(self)

    ############################################################################
    def start(self):
        #input("Press Enter to continue...")

        # Check Liscence
        #from Globals import ini
        #from client.shell.pc.ui.ValidationDialog import validationDialog
        #validationDialog.show(ini.getLsc())
        #ini.setLsc(validationDialog.lsc)

        # create and show main window
        #PYQT#from client.shell.dummy.MainWindow import mainWindow
        #PYQT#mainWindow.show()

        #PYQT#sys.exit(self.app.exec_())

        #PYQT# Comment the following block when UI is used
        try:
            raw_input()
        except:
            input()

    ############################################################################
    def initKernel(self, kernel):
        self.kernel = kernel

    ############################################################################
    def logAdded(self, text):
        print(str(text))

    ############################################################################
    def handle(self, request):
        return self.kernel.handle(request)

    #################################################################################
    def addConfiguration(self, title, getter, setter):
        pass
