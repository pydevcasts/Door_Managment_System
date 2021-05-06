from Lang import lget, CANCEL, NEW_GROUP
from PyQtImports import QWidget, QGridLayout, QHBoxLayout, QPixmap, QLabel, Qt, QSizePolicy
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import mainComponentBorder, noBorder, transparentBackground
from common.shell.ui.dialog.CDialog import CDialog


#################################################################################
#################################################################################
class GroupListDialogWidget(QWidget):

    #############################################################################
    def __init__(self, id_, name, onItemClicked):
        QWidget.__init__(self)

        self.id = id_
        self.onItemClicked = onItemClicked

        self.setStyleSheet(mainComponentBorder())

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        outerWidget = QWidget()
        layout.addWidget(outerWidget, 0, 0, 1, 1)
        outerWidget.setStyleSheet(transparentBackground())

        outerLayout = QGridLayout(outerWidget)
        outerLayout.setSpacing(0)
        outerLayout.setContentsMargins(5, 5, 5, 5)

        innerWidget = QWidget()
        outerLayout.addWidget(innerWidget, 0, 0, 1, 1)
        innerWidget.setStyleSheet(noBorder())

        innerLayout = QHBoxLayout(innerWidget)
        innerLayout.setSpacing(10)
        innerLayout.setContentsMargins(5, 5, 5, 5)

        iconWidget = QLabel()
        pixmap = QPixmap("images/doors.png")
        if id_ == 0:
            pixmap = QPixmap("images/add.png")
        iconWidget.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation))
        innerLayout.addWidget(iconWidget, 0)

        textWidget = QLabel(name)
        textWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        textWidget.setFont(Fonts.GroupFont)
        innerLayout.addWidget(textWidget, 0)

        self.mouseReleaseEvent = self.clicked

    #############################################################################
    def clicked(self, event):
        self.onItemClicked(self.id)


#################################################################################
#################################################################################
class GroupListDialog(CDialog):

    #############################################################################
    def __init__(self, groups):
        CDialog.__init__(self)

        self.group = -1

        self.addSingle(GroupListDialogWidget(0, lget(NEW_GROUP), self.onItemClicked))
        for group in groups:
            if group.id > 0:
                self.addSingle(GroupListDialogWidget(group.id, group.name, self.onItemClicked))

        self.cancelButton = self.addButton(CANCEL)
        self.cancelButton.clicked.connect(self.cancelClicked)

    ############################################################################
    def show(self):
        CDialog.show(self)
        return self._accepted

    #############################################################################
    def onItemClicked(self, id_):
        self.group = id_
        self.close(True)

    #############################################################################
    def cancelClicked(self):
        self.close(False)

    #############################################################################
    def getGroup(self):
        return self.group
