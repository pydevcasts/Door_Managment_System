from Lang import lget, REMOVE_FROM_GROUP, SET_GROUP, GROUP_NAME
from PyQtImports import QWidget, QGridLayout, QHBoxLayout, QLabel, QPixmap, QCursor, Qt
from common.kernel.core.Role import ROLE_OWNER
from common.kernel.request.GroupRequest import GroupRequest
from common.shell.ui.CMenu import CMenu
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import noBorder, whiteBackground, lightGrayBackground, darkGrayForeground
from common.shell.ui.dialog.CTextInputDialog import CTextInputDialog
from server.connection.ConnectionManager import connectionManager
from server.core.DoorList import doorList
from server.ui.GroupListDialog import GroupListDialog


class DoorListWidgetItem(QWidget):

    ############################################################################
    def __init__(self, door, role, onClick):
        QWidget.__init__(self)

        self.door = door
        self.role = role
        self.onClick = onClick

        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)  # (0, 10, 0, 10)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(4, 1)

        self.statusIconWidget = QLabel()
        self.statusIconWidget.setAlignment(Qt.AlignHCenter)

        self.textWidget = QLabel()
        self.textWidget.setFont(Fonts.ListItemFont)
        self.textWidget.setAlignment(Qt.AlignHCenter)
        self.textWidget.setStyleSheet(darkGrayForeground())

        iconsListWidget = QWidget()
        iconsListLayout = QHBoxLayout(iconsListWidget)
        iconsListWidget.setMinimumSize(90, 80)
        iconsListLayout.setAlignment(Qt.AlignCenter)

        self.manipulatedIconWidget = QLabel()
        self.manipulatedIconWidget.setPixmap(QPixmap("images/manipulated.png").scaledToWidth(32))
        self.manipulatedIconWidget.setVisible(False)
        iconsListLayout.addWidget(self.manipulatedIconWidget)

        self.blockedIconWidget = QLabel()
        self.blockedIconWidget.setPixmap(QPixmap("images/blocked.png").scaledToWidth(32))
        self.blockedIconWidget.setVisible(False)
        iconsListLayout.addWidget(self.blockedIconWidget)

        self.errorIconWidget = QLabel()
        iconsListLayout.addWidget(self.errorIconWidget)

        errorReflection = QLabel()
        errorReflection.setMinimumSize(90, 40)

        self.layout.addWidget(QLabel(), 0, 0, 1, 1)
        self.layout.addWidget(errorReflection, 0, 1, 1, 1)
        self.layout.addWidget(self.statusIconWidget, 0, 2, 1, 1)
        self.layout.addWidget(iconsListWidget, 0, 3, 1, 1)
        self.layout.addWidget(QLabel(), 0, 4, 1, 1)
        self.layout.addWidget(self.textWidget, 1, 0, 1, 5)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.contextMenu = CMenu(self)
        setGroupAction = self.contextMenu.addAction(lget(SET_GROUP))
        setGroupAction.triggered.connect(self.setGroup)
        if door.group > 0:
            removeDoorFromGroupAction = self.contextMenu.addAction(lget(REMOVE_FROM_GROUP))
            removeDoorFromGroupAction.triggered.connect(self.removeDoorFromGroup)

        self.mouseReleaseEvent = self.clicked

        self.selected = False
        self.updateUI()

    ############################################################################
    def __str__(self):
        return "DoorListWidgetItem(" + self.door.name + ")"

    ############################################################################
    def __repr__(self):
        return str(self)

    ############################################################################
    def updateUI(self, door=None, selected=None):

        if door is None:
            door = self.door

        if door.serial != self.door.serial:
            return

        self.door = door

        self.textWidget.setText(self.door.name)

        pixmap = QPixmap(self.door.getImageAddress())
        self.statusIconWidget.setPixmap(pixmap)

        pixmap = QPixmap(self.door.getErrorImageAddress())
        self.errorIconWidget.setPixmap(pixmap)

        self.blockedIconWidget.setVisible(door.isBlocked())
        self.manipulatedIconWidget.setVisible(door.isManipulated())

        if selected is None:
            selected = self.selected
        self.select(selected)

    ############################################################################
    def select(self, selected):
        if selected is None:
            return

        self.selected = selected
        if selected:
            self.setStyleSheet(noBorder() + lightGrayBackground())
        else:
            self.setStyleSheet(noBorder() + whiteBackground())

    ############################################################################
    def selectOn(self, serial):
        self.select(self.door.serial == serial)

    #############################################################################
    def clicked(self, event):
        if event.button() == Qt.RightButton:
            return self.showContextMenu(event.pos())

        if self.onClick is not None:
            self.onClick(self)

    #############################################################################
    def showContextMenu(self, point):

        if self.role < ROLE_OWNER:
            return

        self.contextMenu.exec_(self.mapToGlobal(point))

    ##############################################################################
    def setGroup(self):
        groups = doorList.getDoorGroupList()

        request = None

        group = 0
        if len(groups) > 1:
            groupListDialog = GroupListDialog(groups)
            groupListDialog.show()
            if not groupListDialog.isAccepted():
                return
            group = groupListDialog.getGroup()
            request = GroupRequest.update(group, self.door.serial)

        if group > 0 and group == self.door.group:
            return

        if group == 0:
            dialog = CTextInputDialog(None, placeHolder=lget(GROUP_NAME))
            dialog.show()
            if not dialog.isAccepted():
                return

            newName = dialog.getText()
            if newName is None or len(newName.strip()) == 0:
                return
            request = GroupRequest.create(newName, self.door.serial)

        response = connectionManager.get().callRequest(request)
        if response.isSuccessful():
            connectionManager.get().requestEarlyLoad()

    ##############################################################################
    def removeDoorFromGroup(self):
        response = connectionManager.get().callRequest(GroupRequest.update(0, self.door.serial))
        if response.isSuccessful():
            connectionManager.get().requestEarlyLoad()

