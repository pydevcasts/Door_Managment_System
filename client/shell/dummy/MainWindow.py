from PyQtImports import QMainWindow, QWidget, QDesktopWidget, QGridLayout
from common.shell.ui.CAppHeader import CAppHeader
from common.shell.ui.CPushButton import CPushButton


class MainWindow(QMainWindow):

    ############################################################
    def __init__(self):

        QMainWindow.__init__(self)

        from common.shell.AppIcon import appIcon
        self.setWindowIcon(appIcon)

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.header = CAppHeader()
        panel = self.header.install(self, self.centralwidget)

        self.gridLayout = QGridLayout(panel)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(2, 1)

        button = CPushButton("Exit", clicked = self.close)
        self.gridLayout.addWidget(button, 1, 1, 1, 1)

        self.setFixedSize(250, 150)


    ############################################################
    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        w = (resolution.width() / 2) - (self.frameSize().width() / 2)
        h = (resolution.height() / 2) - (self.frameSize().height() / 2)
        self.move(w, h)

    ############################################################
    def show(self):
        self.centerOnScreen()
        QMainWindow.show(self)

############################################################
############################################################
############################################################
mainWindow = MainWindow()
