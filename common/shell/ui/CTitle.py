from PyQtImports import QLabel
from PyQtImports import Qt
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import darkGrayForeground


class CTitle(QLabel):

    def __init__(self, text = None):
        QLabel.__init__(self, text)

        self.setAutoFillBackground(False)

        self.setStyleSheet(darkGrayForeground())

        self.setFont(Fonts.TitleFont)

        self.setAlignment(Qt.AlignBottom)
