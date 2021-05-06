from PyQtImports import QWidget, QGridLayout
from common.shell.ui.UI import mainComponentBorder, whiteBackground
from server.ui.door.DoorTabbedPaneItem import DoorTabbedPaneItem


class DoorTabbedPane(QWidget):

    #############################################################################
    def __init__(self):
        QWidget.__init__(self)

        self.items = []

        layout = QGridLayout(self)
        layout.setRowStretch(0, 1)

        innerWidget = QWidget()
        innerWidget.setStyleSheet(mainComponentBorder() + whiteBackground())
        layout.addWidget(innerWidget, 0, 0, 1, 1)

        self.tabbedPaneLayout = QGridLayout(innerWidget)
        self.tabbedPaneLayout.setColumnStretch(0, 1)

        self.tabbedPaneColumn = 1

    #############################################################################
    def addItem(self, text, imageAddress, onClick, selectable=True):
        item = DoorTabbedPaneItem(self, text, imageAddress, onClick, selectable)
        self.tabbedPaneLayout.addWidget(item, 0, self.tabbedPaneColumn, 1, 1)
        self.tabbedPaneLayout.setColumnStretch(self.tabbedPaneColumn + 1, 1)
        self.tabbedPaneColumn += 2
        self.items.append(item)
        return item

    #############################################################################
    def selectItem(self, item):
        if item is None or not item.selectable:
            return

        for i in self.items:
            i.select(item == i)
