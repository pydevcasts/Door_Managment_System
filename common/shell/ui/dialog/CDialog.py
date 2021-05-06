from PyQtImports import Qt, QDialog, QGridLayout, QWidget, QHBoxLayout, QDesktopWidget, QLabel
from common.shell.ui.CPushButton import CPushButton
from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import lightGrayBackground


################################################################################
################################################################################
class CDialog(QDialog):

    ############################################################################
    def __init__(self):

        QDialog.__init__(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)

        self.setStyleSheet(lightGrayBackground())
        self.setAttribute(Qt.WA_MacShowFocusRect, False)

        # Main Panel & layout
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setColumnStretch(0, 1)

        # North Panel & Layout, for editors
        self.northPanel = CRowPanel()
        self.gridLayout.addWidget(self.northPanel, 0, 0, 1, 1)

        # middle Panel & Layout, for editors
        self.middlePanel = QWidget()
        self.gridLayout.addWidget(self.middlePanel, 1, 0, 1, 1)
        self.middleLayout = QGridLayout(self.middlePanel)
        self.middleLayout.setContentsMargins(0, 0, 0, 0)
        self.middleLayout.setColumnStretch(0, 1)

        # South Panel & Layout, larger than just buttons
        self.southPanel = QWidget()
        self.gridLayout.addWidget(self.southPanel, 2, 0, 1, 1)
        self.southLayout = QGridLayout(self.southPanel)
        self.southLayout.setContentsMargins(0, 0, 0, 0)
        self.southLayout.setColumnStretch(0, 1)
        self.southLayout.setColumnStretch(2, 1)

        # button Panel & Layout, center of south panel, only for buttons
        self.buttonPanel = QWidget()
        self.southLayout.addWidget(self.buttonPanel, 0, 1, 1, 1)
        self.buttonLayout = QHBoxLayout(self.buttonPanel)

        self.setWindowModality(Qt.ApplicationModal)

        self._accepted = False

    ############################################################################
    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        w = (resolution.width() / 2) - (self.frameSize().width() / 2)
        h = (resolution.height() / 2) - (self.frameSize().height() / 2)
        self.move(w, h)

    ############################################################################
    def exec_(self):
        self.setFixedSize(self.sizeHint())
        self.centerOnScreen()
        QDialog.exec_(self)

    ############################################################################
    def show(self):
        self.exec_()

    ############################################################################
    def setFont(self, c):
        if c is None:
            return
        if isinstance(c, QLabel):
            c.setFont(Fonts.DialogTextFont)

    ############################################################################
    def setFonts(self, c1, c2=None, c3=None):
        self.setFont(c1)
        self.setFont(c2)
        self.setFont(c3)

    ############################################################################
    def addSingle(self, c):
        self.setFonts(c)
        self.northPanel.addSingle(c)

    ############################################################################
    def addDouble(self, c1, c2):
        self.setFonts(c1, c2)
        self.northPanel.addDouble(c1, c2)

    ############################################################################
    def addTriple(self, c1, c2, c3):
        self.setFonts(c1, c2, c3)
        self.northPanel.addTriple(c1, c2, c3)

    ############################################################################
    def addButton(self, text):
        button = CPushButton(text)
        button.setFont(Fonts.DialogButtonFont)
        self.buttonLayout.addWidget(button)
        return button

    ############################################################################
    def removeAllButtons(self):
        for i in reversed(range(self.buttonLayout.count())):
            button = self.buttonLayout.itemAt(i).widget()
            self.buttonLayout.removeWidget(button)
            button.setParent(None)

    ############################################################################
    def isAccepted(self):
        return self._accepted

    ############################################################################
    def close(self, accepted=None):
        if accepted is not None:
            self._accepted = accepted
        return QDialog.close(self)
