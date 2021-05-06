from Lang import *
from PyQtImports import Qt, QWidget, QGridLayout, QLabel, QListWidgetItem, QPixmap
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import noBorder, whiteBackground, whiteForeground, darkGrayBackground, darkGrayForeground


class CListWidgetItem(QListWidgetItem):

    ############################################################################
    def __init__(self, titleKey, imageFilePrefix):
        QListWidgetItem.__init__(self)

        self.titleKey = titleKey

        self.pixmap = QPixmap(imageFilePrefix + ".png")
        self.pixmapSelected = QPixmap(imageFilePrefix + "_selected.png")

        self.iconWidget = QLabel()
        self.iconWidget.setAlignment(Qt.AlignHCenter)

        self.textWidget = QLabel()
        self.textWidget.setFont(Fonts.ListItemFont)
        self.textWidget.setAlignment(Qt.AlignHCenter)
        self.textWidget.setStyleSheet(darkGrayForeground())

        self.uiWidget = QWidget()
        self.layout = QGridLayout(self.uiWidget)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(5, 10, 5, 10)  # (0, 10, 0, 10)
        self.layout.setColumnStretch(0, 1)

        self.layout.addWidget(self.iconWidget, 0, 0, 1, 1)
        self.layout.addWidget(self.textWidget, 1, 0, 1, 1)

        lregister(self)

        self.deselect()

        self.setSizeHint(self.uiWidget.sizeHint())

    ############################################################################
    def select(self):
        self.textWidget.setStyleSheet(whiteForeground())
        self.uiWidget.setStyleSheet(noBorder(9) + darkGrayBackground())
        self.iconWidget.setPixmap(self.pixmapSelected)

    ############################################################################
    def deselect(self):
        self.textWidget.setStyleSheet(darkGrayForeground())
        self.uiWidget.setStyleSheet(noBorder(9) + whiteBackground())
        self.iconWidget.setPixmap(self.pixmap)

    ############################################################################
    def setTranslations(self):
        self.textWidget.setText(lget(self.titleKey))
