from PyQtImports import Qt, QCursor
from common.shell.ui.CPushButton import CPushButton
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import whiteBackground, darkGrayForeground, mainComponentBorder


class CLightButton(CPushButton):

    def __init__(self, text = None, iconAddress = None, iconSize = None, clicked = None, translated = False):
        CPushButton.__init__(self, text , iconAddress, iconSize, clicked, translated)
        self.setStyleSheet(whiteBackground() + darkGrayForeground() + mainComponentBorder())
        self.setFont(Fonts.passwordsFont)
        self.setCursor(QCursor(Qt.PointingHandCursor))
