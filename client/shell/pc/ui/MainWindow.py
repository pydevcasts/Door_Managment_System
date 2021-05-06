from Globals import ini, interface
from Lang import lget, lregister, language, APPLICATION_TITLE, COPYRIGHT, VERSION
from PyQtImports import QMainWindow, QWidget, QDesktopWidget, QGridLayout, QLabel, QTextEdit, QStatusBar
from PyQtImports import QPixmap, QTextCursor
from PyQtImports import Qt, QMetaObject, pyqtSignal
from Version import client_version
from client.shell.pc.LogManager import logManager
from common.shell.ui.CAppHeader import CAppHeader
from common.shell.ui.CListWidget import CListWidget
from common.shell.ui.CTitleAndLogo import CTitleAndLogo
from common.shell.ui.UI import lightGrayBackground, mainComponentBorder, whiteBackground


class MainWindow(QMainWindow):
    loginTextUpdater = pyqtSignal(str)
    errorImageUpdater = pyqtSignal(int)

    ############################################################
    def __init__(self):

        QMainWindow.__init__(self)

        from common.shell.AppIcon import appIcon
        self.setWindowIcon(appIcon)

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
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 1)

        self.initListWidget()
        layout.addWidget(self.listWidget, 0, 0, 1, 1)

        rightPanel = QWidget(panel)
        layout.addWidget(rightPanel, 0, 1, 1, 1)
        rightLayout = QGridLayout(rightPanel)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setSpacing(0)
        rightLayout.setColumnStretch(0, 1)
        rightLayout.setRowStretch(1, 1)

        self.titleWidget = CTitleAndLogo()
        rightLayout.addWidget(self.titleWidget, 0, 0, 1, 1)

        itemPanel = QWidget(rightPanel)
        self.itemLayout = QGridLayout(itemPanel)
        self.itemLayout.setContentsMargins(0, 0, 0, 0)
        self.itemLayout.setSpacing(0)
        self.itemLayout.setColumnStretch(0, 1)
        self.itemLayout.setRowStretch(0, 1)
        rightLayout.addWidget(itemPanel, 1, 0, 1, 1)

        # Initial Selection
        from client.shell.pc.ItemPack import items
        self.setLastItem(items[0])
        self.listWidget.setCurrentItem(items[0].listWidgetItem)

        self.logWidget = QTextEdit()
        self.logWidget.setReadOnly(True)
        self.logWidget.setStyleSheet(whiteBackground() + mainComponentBorder())
        layout.addWidget(self.logWidget, 1, 0, 1, 2)

        self.initLanguageBar()

        # self.resize(800, 700)
        self.setFixedSize(1000, 800)

        QMetaObject.connectSlotsByName(self)

        logManager.updateUiLog.connect(self.updateLogs)
        self.updateLogs(logManager.getHtmlText())

        self.loginTextUpdater.connect(self.updateLoginTextSlot)

        self.errorImageUpdater.connect(self.updateErrorImageSlot)
        self.updateDoorError(0, 0)
        interface.get().addDoorErrorListener(self)

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
    def initStatusBar(self):
        self.statusbar = QStatusBar()

        self.copyrightLabel = QLabel()
        self.statusbar.addWidget(self.copyrightLabel)

        self.loginStatus = QLabel()
        self.statusbar.addWidget(self.loginStatus)

        self.errorImage = QLabel()
        self.statusbar.addPermanentWidget(self.errorImage)
        self.statusbar.addPermanentWidget(QLabel("  "))

        self.versionLabel = QLabel()
        self.statusbar.addPermanentWidget(self.versionLabel)

    ############################################################
    def initListWidget(self):

        self.listWidget = CListWidget()
        # self.listWidget.setMinimumSize(170, 300)
        # self.listWidget.setMaximumSize(170, 800)
        self.listWidget.setFixedSize(170, 485)
        self.listWidget.setObjectName("listWidget")

        # Add widget to QListWidget funList
        from client.shell.pc.ItemPack import items
        for item in items:
            self.listWidget.addItem(item.listWidgetItem)
            self.listWidget.setItemWidget(item.listWidgetItem, item.listWidgetItem.uiWidget)

        self.listWidget.currentItemChanged['QListWidgetItem*', 'QListWidgetItem*'] \
            .connect(self.listItemChanged)

    ############################################################
    def initLanguageBar(self):
        self.header.addButton("images/en.png", onClick=language.english)
        self.header.addButton("images/de.png", onClick=language.german)
        self.header.addButton("images/es.png", onClick=language.spanish)
        # self.header.addButton("images/fa.png", onClick = language.persian)

        lregister(self)
        language.notify()

    ############################################################
    def setTranslations(self):
        self.setWindowTitle(lget(APPLICATION_TITLE))
        self.copyrightLabel.setText("<html>" + lget(COPYRIGHT) + "</html>")
        self.versionLabel.setText(
            "<html><span style=\"color:blue;\">" + lget(VERSION) + " " + client_version + "</span></html>")
        self.titleWidget.setText(lget(self.lastItem.titleKey))

    ############################################################
    def listItemChanged(self, selectedWidgetItem):

        if selectedWidgetItem is None:
            return

        # Add widget to QListWidget funList
        from client.shell.pc.ItemPack import items

        selectedItem = None
        for item in items:
            if selectedWidgetItem == item.listWidgetItem:
                selectedItem = item
                break

        if selectedItem is None:
            return

        if selectedItem == self.lastItem:
            return

        if not selectedItem.ItemPanel.selectionAccepted():
            self.listWidget.setCurrentItem(self.lastItem.listWidgetItem)
            return

        self.removeItem(self.lastItem)
        self.setLastItem(item)

    ############################################################
    def removeItem(self, item):
        self.titleWidget.setText("")

        if item is None:
            return
        item.unselect()

        if item.ItemPanel is None:
            return
        self.itemLayout.removeWidget(item.ItemPanel)
        item.ItemPanel.setParent(None)

    ############################################################
    def setLastItem(self, item):
        if item is None:
            return

        item.select()
        self.titleWidget.setText(lget(item.titleKey))

        if item.ItemPanel is not None:
            self.itemLayout.addWidget(item.ItemPanel, 0, 0, 1, 1)
        self.lastItem = item

    ############################################################
    def updateLogs(self, htmlText):
        self.logWidget.clear()
        self.logWidget.textCursor().insertHtml(htmlText)
        self.logWidget.moveCursor(QTextCursor.End)

    ####################################################################################
    def updateLoginText(self, loginText):
        self.loginTextUpdater.emit(loginText)

    ############################################################
    def updateLoginTextSlot(self, loginText):
        self.loginStatus.setText("            " + loginText)

    ####################################################################################
    def updateDoorError(self, errorCode, errorTime):
        self.errorImageUpdater.emit(errorCode)

    ############################################################
    def updateErrorImageSlot(self, errorCode):
        imageName = "error_ok"
        if errorCode >= 240:
            imageName = "error_absolute"
        elif errorCode >= 210:
            imageName = "error_critical"
        elif errorCode >= 100:
            imageName = "error_common"
        elif errorCode >= 10:
            imageName = "error_info"

        pixmap = QPixmap("images/" + imageName + ".png")
        self.errorImage.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.FastTransformation))

    ############################################################
    def closeEvent(self, event):
        # result = QtGui.QMessageBox.question(self,
        #              "Confirm Exit...",
        #              "Are you sure you want to exit ?",
        #              QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        # if (result)
        #    event.ignore()

        ini.save()

        from Exit import exit
        exit.exit()

        QMainWindow.closeEvent(self, event)


############################################################
############################################################
############################################################
mainWindow = MainWindow()
