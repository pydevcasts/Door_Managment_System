from Globals import logger
from PyQtImports import QPixmap, QCursor
from PyQtImports import QWidget, QGridLayout, QLabel
from PyQtImports import Qt
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import noBorder, darkGrayForeground, whiteBackground, lightGrayBackground


class DoorTabbedPaneItem(QWidget):

    #############################################################################
    def __init__(self, doorTabbedPane, text, imageAddress, onClick, selectable):
        QWidget.__init__(self)

        self.doorTabbedPane = doorTabbedPane

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setColumnStretch(0, 1)

        iconWidget = QLabel()
        iconWidget.setAlignment(Qt.AlignHCenter)
        iconWidget.setPixmap(QPixmap(imageAddress))

        textWidget = QLabel()
        textWidget.setFont(Fonts.ListItemFont)
        textWidget.setAlignment(Qt.AlignHCenter)
        textWidget.setStyleSheet(darkGrayForeground())
        textWidget.setText(text)

        layout.addWidget(self.createDummyLabel(), 0, 0, 2, 1)
        layout.addWidget(iconWidget, 0, 1, 1, 1)
        layout.addWidget(textWidget, 1, 1, 1, 1)
        layout.addWidget(self.createDummyLabel(), 0, 2, 2, 1)

        self.onClick = onClick
        self.selectable = selectable

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.select(False)

        self.mouseReleaseEvent = self.clicked
        iconWidget.mouseReleaseEvent = self.clicked
        textWidget.mouseReleaseEvent = self.clicked

    #############################################################################
    def createDummyLabel(self):
        label = QLabel()
        label.setMinimumSize(5, 5)
        return label

    #############################################################################
    def select(self, selected=True):
        if selected:
            self.setStyleSheet(noBorder() + lightGrayBackground())
        else:
            self.setStyleSheet(noBorder() + whiteBackground())

    #############################################################################
    def clicked(self, event):
        try:
            self.doorTabbedPane.selectItem(self)
        except:
            pass

        if self.onClick is not None:
            try:
                self.onClick()
            except:
                import traceback
                logger.exception(traceback.format_exc())
