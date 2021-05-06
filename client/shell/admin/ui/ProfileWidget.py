from PyQtImports import QWidget, QGridLayout, QLabel
from PyQtImports import pyqtSignal
from common.shell.ui.CPushButton import CPushButton


class ProfileWidget(QWidget):
    onMouseLeave = pyqtSignal()
    onMouseEnter = pyqtSignal()

    def __init__(self, mainWindow, profileName):
        QWidget.__init__(self)

        self.mainWindow = mainWindow
        self.profileName = profileName

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setColumnStretch(0, 1)

        from common.shell.ui.UI import grayBackground
        self.setStyleSheet(grayBackground())

        self.label = QLabel("    " + profileName)
        self.label.setMinimumSize(100, 30)
        self.layout.addWidget(self.label, 0, 0, 1, 1)

        self.deleteButton = CPushButton(iconAddress="images/delete16", iconSize=16, clicked=self.deleteButtonClicked)
        self.deleteButton.setVisible(False)
        self.layout.addWidget(self.deleteButton, 0, 1, 1, 1)

    def deleteButtonClicked(self):
        self.mainWindow.deleteProfile(self.profileName)

    def mousePressEvent(self, event):
        self.mainWindow.loadProfile(self.profileName)

    def leaveEvent(self, e):
        self.deleteButton.setVisible(False)

    def enterEvent(self, e):
        self.deleteButton.setVisible(True)
