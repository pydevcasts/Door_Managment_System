from Lang import lget, lregister
from PyQtImports import QPixmap, QCursor, QMovie
from PyQtImports import QWidget, QGridLayout, QLabel
from PyQtImports import Qt, QMetaObject, pyqtSignal
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import orangeBackground, whiteBackground, noBorder, mainComponentBorder, darkGrayForeground


class CStatusButton(QWidget):
    updateUiSignal = pyqtSignal()

    #######################################################################################
    def __init__(self, baseStatus, onClick):

        QWidget.__init__(self)

        self.onClick = onClick

        self.innerPanel = QWidget()
        self.innerPanel.setFixedSize(200, 60)
        innerLayout = QGridLayout(self.innerPanel)
        innerLayout.setContentsMargins(0, 0, 0, 0)
        innerLayout.setSpacing(5)
        innerLayout.setColumnStretch(2, 1)

        self.image = QLabel(self.innerPanel)
        innerLayout.addWidget(self.image, 0, 0, 1, 1)  # self.image.setGeometry(QtCore.QRect(0, 0, 90, 60))

        self.textLabel = QLabel(self.innerPanel)
        self.textLabel.setStyleSheet(darkGrayForeground())
        innerLayout.addWidget(self.textLabel, 0, 1, 1, 1)  # self.textLabel.setGeometry(QtCore.QRect(100, 0, 200, 60))

        self.middlePanel = QWidget()
        middleLayout = QGridLayout(self.middlePanel)
        middleLayout.setContentsMargins(5, 5, 5, 5)
        middleLayout.setSpacing(0)
        middleLayout.setColumnStretch(0, 1)
        middleLayout.setColumnStretch(2, 1)
        middleLayout.setRowStretch(0, 1)
        middleLayout.setRowStretch(2, 1)

        middleLayout.addWidget(self.innerPanel, 1, 1, 1, 1)

        outerLayout = QGridLayout(self)
        outerLayout.setContentsMargins(0, 0, 0, 0)
        outerLayout.setSpacing(0)

        outerLayout.addWidget(self.middlePanel, 0, 0, 1, 1)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setBaseStatus(baseStatus)

        QMetaObject.connectSlotsByName(self)
        self.updateUiSignal.connect(self.updateUiSlot)

        lregister(self)

        self.selected = True
        self.unselect()

    #######################################################################################
    def setBaseStatus(self, baseStatus):
        self.baseStatus = baseStatus
        self.setTranslations()

    #######################################################################################
    def setTranslations(self):
        if self.baseStatus is not None:
            self.textLabel.setText(lget(self.baseStatus.text))

    #######################################################################################
    def unselect(self, baseStatus=None):

        if self.baseStatus == baseStatus:
            baseStatus = None

        if baseStatus is not None:
            self.setBaseStatus(baseStatus)
        elif not self.selected:
            return

        self.selected = False
        self.updateUI()

    #######################################################################################
    def select(self, baseStatus=None):
        if self.baseStatus == baseStatus:
            baseStatus = None

        if baseStatus is not None:
            self.setBaseStatus(baseStatus)
        elif self.selected:
            return

        self.selected = True
        self.updateUI()

    #######################################################################################
    def updateUI(self):
        self.updateUiSignal.emit()

    #######################################################################################
    def updateUiSlot(self):
        if self.selected:
            return self.applyToUi(orangeBackground(), Fonts.StatusFontFocused, self.enableAnimation)

        return self.applyToUi(whiteBackground(), Fonts.StatusFont, self.enablePixmap)

    #######################################################################################
    def applyToUi(self, backgroundStyle, textFont, enableImageFunction):
        # self.setStyleSheet("border: 5px solid blue")
        self.setStyleSheet(self.defaultStyle())
        self.middlePanel.setStyleSheet(backgroundStyle)
        self.innerPanel.setStyleSheet(noBorder())
        self.textLabel.setFont(textFont)
        enableImageFunction()

    #######################################################################################
    def defaultStyle(self):
        return mainComponentBorder()

    #######################################################################################
    def enablePixmap(self):
        if self.baseStatus is None:
            return

        pixmap = QPixmap(self.baseStatus.imageAddress)
        self.image.setPixmap(pixmap)

    #######################################################################################
    def enableAnimation(self):
        if self.baseStatus is None:
            return

        if self.baseStatus.animationAddress is None:
            return self.enablePixmap()

        movie = QMovie(self.baseStatus.animationAddress)
        self.image.setMovie(movie)
        movie.start()

    #######################################################################################
    def mousePressEvent(self, event):
        try:
            self.onClick(self.baseStatus)
        except:
            pass
