from PyQtImports import QWidget, QGridLayout
from common.shell.ui.CRowLayout import CRowLayout


class CRowPanel(QWidget):

    ##############################################################################
    def __init__(self):
        QWidget.__init__(self)

        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(0)
        gridLayout.setRowStretch(1, 1)
        gridLayout.setColumnStretch(0, 1)

        self.topPanel = QWidget()
        self.layout = CRowLayout(self.topPanel)
        gridLayout.addWidget(self.topPanel, 0, 0, 1, 1)
    """
    def __init2__(self):
        QWidget.__init__(self)

        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        scroll = QScrollArea(self)
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        self.topPanel = QWidget(scroll)
        self.layout = CRowLayout(self.topPanel)
        scroll.setWidget(self.topPanel)
    """

    ##############################################################################
    def addTriple(self, label, display, edit):
        self.layout.addTriple(label, display, edit)

    ##############################################################################
    def addDouble(self, label, editor):
        self.layout.addDouble(label, editor)

    ##############################################################################
    def addSingle(self, widget, rowCount = 1):
        self.layout.addSingle(widget, rowCount)

    ##############################################################################
    def addCenter(self, widget, rowCount = 1):
        self.layout.addCenter(widget, rowCount)

    ##############################################################################
    def setContentsMargins(self, a, b, c, d):
        self.layout.setContentsMargins(a, b, c, d)

    ##############################################################################
    def setSpacing(self, s):
        self.layout.setSpacing(s)

    ##############################################################################
    def setRowStretch(self, row, i):
        self.layout.setRowStretch(row, i)

    ##############################################################################
    def setColumnStretch(self, column, i):
        self.layout.setColumnStretch(column, i)

    ##############################################################################
    def clear(self):
        self.layout.clear()