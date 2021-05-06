from PyQtImports import QGridLayout


class CRowLayout(QGridLayout):

    ##############################################################################
    def __init__(self, widget):
        QGridLayout.__init__(self, widget)

        self.setContentsMargins(2, 2, 2, 2)
        self.setSpacing(10)
        self.setColumnStretch(2, 1)

        self.row = 0

    ##############################################################################
    def addTriple(self, label, display, edit):

        if label is not None:
            self.addWidget(label, self.row, 0, 1, 1)
        if display is not None:
            self.addWidget(display, self.row, 1, 1, 2)
        if edit is not None:
            self.addWidget(edit, self.row, 3, 1, 1)
        self.row = self.row + 1

    ##############################################################################
    def addDouble(self, label, editor):

        if label is not None:
            self.addWidget(label, self.row, 0, 1, 1)
        if editor is not None:
            self.addWidget(editor, self.row, 1, 1, 3)
        self.row = self.row + 1

    ##############################################################################
    def addSingle(self, widget, rowCount=1):

        if widget is not None:
            self.addWidget(widget, self.row, 0, rowCount, 4)
            self.row = self.row + rowCount

    ##############################################################################
    def addCenter(self, widget, rowCount=1):

        self.addWidget(widget, self.row, 1, rowCount, 1)
        self.row = self.row + rowCount

    ##############################################################################
    def clear(self):
        for i in reversed(range(self.count())):
            child = self.takeAt(i)
            if child.widget():
                child.widget().setParent(None)
        self.row = 0
