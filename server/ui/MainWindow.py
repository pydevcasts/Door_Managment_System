import threading
import time

from Lang import lget, APPLICATION_TITLE, COPYRIGHT, VERSION
from PyQtImports import QMainWindow, QWidget, QDesktopWidget, QGridLayout, QLabel, QStatusBar, pyqtSignal
from Version import server_version
from common.shell.ui.CAppHeader import CAppHeader
from common.shell.ui.CPushButton import CPushButton
from common.shell.ui.UI import lightGrayBackground, blackForeground, redForeground
from server.connection.ConnectionManager import connectionManager
from server.ui.door.DoorPanel import DoorPanel
from server.ui.list.GroupListWidget import GroupListWidget


class MainWindow(QMainWindow):
    closePanelSignal = pyqtSignal()
    alertSignal = pyqtSignal()

    ############################################################
    def __init__(self):

        QMainWindow.__init__(self)

        self.setWindowTitle(lget(APPLICATION_TITLE))

        from common.shell.AppIcon import appIcon
        self.setWindowIcon(appIcon)

        from ExceptHook import myExceptionHook
        myExceptionHook.addHandle(self.handleUnexpectedError)

        self.initStatusBar()
        self.setStatusBar(self.statusbar)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet(lightGrayBackground())

        self.header = CAppHeader()
        panel = self.header.install(self, self.centralWidget)

        layout = QGridLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(25)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 7)
        layout.setRowStretch(0, 1)

        westPanel = QWidget(panel)
        westLayout = QGridLayout(westPanel)
        westLayout.setContentsMargins(0, 0, 0, 0)
        westLayout.setSpacing(25)
        westLayout.setColumnStretch(0, 1)
        westLayout.setRowStretch(1, 1)
        layout.addWidget(westPanel, 0, 0, 1, 1)

        connectionButton = CPushButton("Connection", clicked=self.connectionButtonClicked)
        westLayout.addWidget(connectionButton, 0, 0, 1, 1)

        self.initListWidget()
        westLayout.addWidget(self.listWidget, 1, 0, 1, 1)

        eastPanel = QWidget(panel)
        self.eastLayout = QGridLayout(eastPanel)
        self.eastLayout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(eastPanel, 0, 1, 1, 1)

        # self.resize(2500, 1600)
        self.resize(1450, 800)

        self.currentPanel = None

        self.closePanelSignal.connect(self.closePanelSlot)
        self.alertSignal.connect(self.alertSlot)

        self.alertText = None
        self.alertTime = None
        self.alertError = None
        threading.Thread(target=self.alertThread, daemon=True).start()

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

        if not connectionManager.check():
            self.connectionButtonClicked()

    ############################################################
    def connectionButtonClicked(self):
        from server.ui.ConnectionDialog import connectionDialog
        connectionDialog.show()

    ############################################################
    def initStatusBar(self):
        self.statusbar = QStatusBar()

        copyrightLabel = QLabel("<html>" + lget(COPYRIGHT) + "</html>")
        self.statusbar.addWidget(copyrightLabel)

        self.alertWidget = QLabel()
        self.statusbar.addWidget(self.alertWidget)

        versionLabel = QLabel("<html><span style=\"color:blue;\">" + lget(VERSION) + " " + server_version + "</span></html>")
        self.statusbar.addPermanentWidget(versionLabel)

    ############################################################
    def initListWidget(self):

        self.listWidget = GroupListWidget()
        self.listWidget.setMinimumSize(430, 600)

        self.listWidget.setSelectedDoorItemValidator(self)

    ############################################################
    def validateSelectedDoorItem(self, door):

        if door is None:
            self.closePanel()
            return True

        if self.currentPanel is not None and self.currentPanel.serial == door.serial:
            return True

        if not door.isConnectionValid():
            from common.shell.ui.dialog.CAlertDialog import CAlertDialog
            CAlertDialog("Door is in invalid state").show()
            return False

        if not connectionManager.get().prepareDoorForDisplay(door):
            return False

        # display a waiting dialog
        #

        from server.exception.DmsException import DmsException
        try:
            # call LoadDoor service
            from common.kernel.request.DoorRequest import DoorRequest
            request = DoorRequest()
            doorResponse = connectionManager.get().callRequest(request, door)
            door.update(doorResponse)

            self.openDoor(door.serial, doorResponse.role)
            # close waiting dialog
            #
        except DmsException as err:
            # close waiting dialog
            #
            door.password = None
            from common.shell.ui.dialog.CAlertDialog import CAlertDialog
            CAlertDialog(err).show()
            return False

        return True

    ############################################################
    def openDoor(self, serial, role):

        # select DoorListWidgetItem
        self.listWidget.select(serial)

        # create door panel and display it
        doorPanel = DoorPanel(serial, role, self.alert)
        self.addPanel(doorPanel)

    ############################################################
    def addPanel(self, doorPanel):
        if doorPanel == self.currentPanel:
            return

        self.closePanel()
        self.currentPanel = doorPanel
        self.eastLayout.addWidget(doorPanel, 0, 0, 1, 1)

    ############################################################
    def closePanel(self):
        if self.currentPanel is None:
            return
        self.closePanelSignal.emit()

    ############################################################
    def closePanelSlot(self):
        if self.currentPanel is None:
            return
        self.eastLayout.removeWidget(self.currentPanel)
        self.currentPanel.setParent(None)
        self.currentPanel = None

    ############################################################
    def alert(self, text, error=False):
        self.alertText = text
        self.alertTime = time.time()
        self.alertError = error

    ############################################################
    def alertThread(self):
        while True:
            try:
                self.alertSignal.emit()
            finally:
                time.sleep(0.2)

    ############################################################
    def alertSlot(self):

        if self.alertTime is not None and time.time() - self.alertTime > 5:
            self.alertWidget.setText("")
            self.alertTime = None
            return

        if self.alertError is None:
            return

        self.alertWidget.setText("       " + lget(str(self.alertText)) + "       ")
        if self.alertError:
            self.alertWidget.setStyleSheet(redForeground())
        else:
            self.alertWidget.setStyleSheet(blackForeground())
        self.alertError = None

    ############################################################
    def handleUnexpectedError(self, error):
        self.alert("Internal Error! will be logged on our servers.", True)


################################################################
################################################################
################################################################
mainWindow = MainWindow()
