from PyQtImports import QIcon, QSize, Qt
from PyQtImports import QWidget, QGridLayout, QLabel, QPushButton
from common.shell.ui.UI import whiteBackground, noBorder


class CAppHeader(QWidget):

    ################################################################################
    def __init__(self, showButtons=True):
        QWidget.__init__(self)

        self.frame = None
        self.offset = None

        innerPanel = QWidget()
        innerLayout = QGridLayout(innerPanel)
        innerLayout.setSpacing(0)
        innerLayout.setContentsMargins(0, 0, 0, 0)
        innerLayout.setColumnStretch(1, 1)

        self.leftIndex = 0
        leftPanel = QWidget()
        self.leftLayout = QGridLayout(leftPanel)
        self.leftLayout.setSpacing(0)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        innerLayout.addWidget(leftPanel, 0, 0, 1, 1)

        dummyLabel = QLabel()
        dummyLabel.setMinimumSize(30, 30)
        innerLayout.addWidget(dummyLabel, 0, 1, 1, 1)

        rightPanel = QWidget()
        rightLayout = QGridLayout(rightPanel)
        rightLayout.setSpacing(0)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        innerLayout.addWidget(rightPanel, 0, 2, 1, 1)

        self.maximized = False

        self.minimizeButton = self.createButton("images/minimizebutton24.png")
        self.maximizeButton = self.createButton("images/maximizebutton24.png")
        self.closeButton = self.createButton("images/closebutton24.png")
        if showButtons:
            rightLayout.addWidget(self.minimizeButton, 0, 0, 1, 1)
            rightLayout.addWidget(self.maximizeButton, 0, 1, 1, 1)
            rightLayout.addWidget(self.closeButton, 0, 2, 1, 1)

        innerPanel.setStyleSheet(whiteBackground() + noBorder(8))

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setColumnStretch(0, 1)
        layout.addWidget(innerPanel, 0, 0, 1, 1)

    ################################################################################
    def createButton(self, imageAddress=None, text=None, onClick=None):

        button = QPushButton()
        button.setStyleSheet("border: none; outline:0;")

        if imageAddress is not None:
            button.setIcon(QIcon(imageAddress))
            button.setIconSize(QSize(24, 24))

        if text is not None:
            button.setText(text)

        if onClick is not None:
            button.clicked.connect(onClick)

        return button

    ################################################################################
    def addButton(self, imageAddress=None, text=None, onClick=None):

        button = self.createButton(imageAddress, text, onClick)
        self.leftLayout.addWidget(button, 0, self.leftIndex, 1, 1)
        self.leftIndex += 1

        return button

    ################################################################################
    def install(self, frame, widget=None):

        if widget is None:
            widget = frame

        self.frame = frame

        outerLayout = QGridLayout(widget)
        outerLayout.setSpacing(20)
        outerLayout.setContentsMargins(20, 20, 20, 20)
        outerLayout.setRowStretch(1, 1)

        outerLayout.addWidget(self, 0, 0, 1, 1)

        resultWidget = QWidget()
        outerLayout.addWidget(resultWidget, 1, 0, 1, 1)

        self.minimizeButton.clicked.connect(frame.showMinimized)
        self.maximizeButton.clicked.connect(self.onMaximize)
        self.closeButton.clicked.connect(frame.close)
        frame.setWindowFlags(Qt.CustomizeWindowHint)  # FramelessWindowHint

        return resultWidget

    def onMaximize(self):
        if self.maximized:
            self.frame.showNormal()
            self.maximizeButton.setIcon(QIcon("images/unmaximizebutton24.png"))
        else:
            self.frame.showMaximized()
            self.maximizeButton.setIcon(QIcon("images/maximizebutton24.png"))

        self.maximized = not self.maximized

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.frame.move(x - x_w, y - y_w)
