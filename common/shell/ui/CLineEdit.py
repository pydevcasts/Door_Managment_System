from PyQtImports import QLineEdit
from common.shell.ui.Constants import Constants
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import whiteBackground, littleComponentBorder


class CLineEdit(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)
        self.setMinimumSize(1, Constants.DEFAULT_EDITOR_HEIGHT)
        self.setMaximumSize(Constants.INFINITY_SIZE, Constants.DEFAULT_EDITOR_HEIGHT)
        self.setFont(Fonts.DisplayFont)
        self.setStyleSheet(whiteBackground() + littleComponentBorder())

    def setText(self, text):
        try:
            QLineEdit.setText(self, text)
        except:
            if text is None:
                QLineEdit.setText(self, '')
            else:
                QLineEdit.setText(self, str(text))
