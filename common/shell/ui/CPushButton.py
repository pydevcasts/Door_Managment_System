from Lang import lget, lregister
from PyQtImports import QIcon
from PyQtImports import QPushButton
from PyQtImports import QSize
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import grayBackground, darkGrayBackground, whiteForeground, noBorder, padding


class CPushButton(QPushButton):

    def __init__(self, text=None, iconAddress=None, iconSize=None, clicked=None, translated=False):
        QPushButton.__init__(self, text)

        self.text = text
        if text is not None:
            self.setTranslations()
            if translated:
                lregister(self)

        if iconAddress is not None:
            self.setIcon(QIcon(iconAddress))
        if iconSize is not None:
            self.setIconSize(QSize(iconSize, iconSize))
        if clicked is not None:
            self.clicked.connect(clicked)

        self.setFont(Fonts.CommandFont)

        baseStyle = whiteForeground() + noBorder(8) + padding(5) + "outline:0; min-width:80px; min-height: 25px;"
        defaultStyle = "QPushButton {" + baseStyle + darkGrayBackground() + "}"
        hoverStyle = " QPushButton:hover {" + baseStyle + grayBackground() + "}"

        self.setStyleSheet(defaultStyle + hoverStyle)

        """
            border-radius: 6px;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #f6f7fa, stop: 1 #dadbde);
        """

    def setTranslations(self):
        self.setText(lget(self.text))
