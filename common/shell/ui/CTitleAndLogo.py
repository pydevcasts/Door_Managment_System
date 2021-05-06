from PyQtImports import QPixmap
from PyQtImports import QWidget, QGridLayout, QLabel
from common.shell.ui.CTitle import CTitle


class CTitleAndLogo(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        layout = QGridLayout(self)

        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 0)

        self.title = CTitle()
        layout.addWidget(self.title, 0, 0, 1, 1)

        pixmap = QPixmap('images/appheader.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        layout.addWidget(logo, 0, 2, 1, 1)

    def setText(self, text):
        self.title.setText(text)
