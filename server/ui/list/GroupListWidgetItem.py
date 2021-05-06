from Lang import lget, RENAME_GROUP, GROUP_NAME, DELETE_GROUP
from PyQtImports import QWidget, QVBoxLayout, QHBoxLayout, Qt, QLabel, QPixmap, QSizePolicy, pyqtSignal, QScrollArea, \
    QFrame
from common.kernel.core.DoorErrors import doorErrors
from common.kernel.core.Role import ROLE_OWNER
from common.kernel.request.GroupRequest import GroupRequest
from common.shell.ui.CMenu import CMenu
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import noBorder, whiteBackground, darkGrayBackground, whiteForeground
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog
from common.shell.ui.dialog.CTextInputDialog import CTextInputDialog
from server.ui.list.DoorListWidgetItem import DoorListWidgetItem


class GroupListWidgetItem(QWidget):

    expandOnSignal = pyqtSignal(int)

    ##############################################################################
    def __init__(self, group, groupListWidget):
        QWidget.__init__(self)

        self.group = group
        self.GroupListWidget = groupListWidget
        self.expanded = None

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.headerWidget = QWidget()
        self.headerWidget.setStyleSheet(darkGrayBackground())
        headerLayout = QHBoxLayout(self.headerWidget)
        layout.addWidget(self.headerWidget, 0)
        self.headerWidget.mouseReleaseEvent = self.headerClicked

        self.headerText = QLabel()
        self.headerText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.headerText.setAlignment(Qt.AlignCenter)
        self.headerText.setMinimumSize(25, 25)
        self.headerText.setFont(Fonts.GroupFont)
        self.headerText.setStyleSheet(darkGrayBackground() + whiteForeground())
        headerLayout.addWidget(self.headerText, 1)

        self.manipulatedIcon = QLabel()
        self.manipulatedIcon.setPixmap(QPixmap("images/manipulated.png").scaledToWidth(32))
        headerLayout.addWidget(self.manipulatedIcon, 0)

        self.blockedIcon = QLabel()
        self.blockedIcon.setPixmap(QPixmap("images/blocked.png").scaledToWidth(32))
        headerLayout.addWidget(self.blockedIcon, 0)

        self.lockedIcon = QLabel()
        self.lockedIcon.setPixmap(QPixmap("images/locked_doors.png").scaledToWidth(32))
        headerLayout.addWidget(self.lockedIcon, 0)

        self.openIcon = QLabel()
        self.openIcon.setPixmap(QPixmap("images/open_doors.png").scaledToWidth(32))
        headerLayout.addWidget(self.openIcon, 0)

        self.errorIcon = QLabel()
        headerLayout.addWidget(self.errorIcon, 0)

        scrollInsideWidget = QWidget()
        scrollInsideLayout = QVBoxLayout(scrollInsideWidget)

        self.scroll = QScrollArea()
        self.scroll.setWidget(scrollInsideWidget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        layout.addWidget(self.scroll, 1)

        self.doorsWidget = QWidget()
        self.doorLayout = QVBoxLayout(self.doorsWidget)
        self.doorLayout.setSpacing(20)
        self.doorLayout.setContentsMargins(0, 0, 0, 0)
        scrollInsideLayout.addWidget(self.doorsWidget, 0)

        self.dummyWidget = QWidget()
        scrollInsideLayout.addWidget(self.dummyWidget, 1)

        self.contextMenu = CMenu(self)
        renameGroupAction = self.contextMenu.addAction(lget(RENAME_GROUP))
        renameGroupAction.triggered.connect(self.renameGroup)
        deleteGroupAction = self.contextMenu.addAction(lget(DELETE_GROUP))
        deleteGroupAction.triggered.connect(self.deleteGroup)

        self.setStyleSheet(noBorder() + whiteBackground())

        self.expandOn(0)

        self.updateUI(group)

    ###############################################################################
    def __repr__(self):
        return "GroupListWidgetItem<" + str(self.group) + ">"

    #############################################################################
    def setHeaderVisible(self, visible):
        self.headerWidget.setVisible(visible)

    #############################################################################
    def expandOn(self, id):
        toBeExpanded = id == self.group.id
        if toBeExpanded == self.expanded:
            return

        self.scroll.setVisible(toBeExpanded)
        self.expanded = toBeExpanded

    #############################################################################
    def selectOn(self, serial):
        for index in range(0, self.doorLayout.count()):
            doorItem = self.doorLayout.itemAt(index).widget()
            doorItem.selectOn(serial)

    #############################################################################
    def headerClicked(self, event):
        if event.button() == Qt.RightButton:
            return self.showContextMenu(event.pos())

        if self.expanded:
            return
        self.GroupListWidget.onGroupItemClicked(self)

    #############################################################################
    def showContextMenu(self, point):
        if self.group.id == 0:
            return
        if self.group.role < ROLE_OWNER:
            return

        self.contextMenu.exec_(self.mapToGlobal(point))

    ##############################################################################
    def updateUI(self, doorGroup):
        if doorGroup is None:
            return

        self.headerText.setText(doorGroup.name)

        doorMap = {}

        doorItemList = doorGroup.doorList
        open_door = False
        locked_door = False
        blocked_door = False
        manipulated_door = False
        errorCode = -1
        for door in doorItemList:
            doorMap[door.serial] = door
            open_door = open_door or door.isInOpenStatus()
            locked_door = locked_door or door.isInLockedStatus()
            blocked_door = blocked_door or door.isBlocked()
            manipulated_door = manipulated_door or door.isManipulated()
            if door.doorError > errorCode:
                errorCode = door.doorError

        self.openIcon.setVisible(open_door)
        self.lockedIcon.setVisible(locked_door)

        self.blockedIcon.setVisible(blocked_door)
        self.manipulatedIcon.setVisible(manipulated_door)

        pixmap = QPixmap(doorErrors.getImageAddress(errorCode))
        self.errorIcon.setPixmap(pixmap)

        removeArr = []

        for index in range(0, self.doorLayout.count()):
            doorItem = self.doorLayout.itemAt(index).widget()

            serial = doorItem.door.serial
            if serial not in doorMap:
                removeArr = [doorItem] + removeArr
                continue

            doorItem.updateUI(doorMap.pop(serial, None))
            if doorItem.selected and not doorItem.door.isConnectionValid():
                self.GroupListWidget.validateSelectedDoorItem(None)

        # remove items which are not existing any more
        for doorItem in removeArr:
            if doorItem.selected:
                self.GroupListWidget.validateSelectedDoorItem(None)
            self.doorLayout.removeWidget(doorItem)
            doorItem.setParent(None)

        # add the remaining items in doorMap, these are the new doors
        for door in doorMap.values():
            doorItem = DoorListWidgetItem(door, doorGroup.role, self.GroupListWidget.onDoorItemClicked)
            self.doorLayout.addWidget(doorItem, 0)

    ##############################################################################
    def renameGroup(self):
        dialog = CTextInputDialog(None, placeHolder=lget(GROUP_NAME), defaultText=self.group.name)
        dialog.show()
        if not dialog.isAccepted():
            return

        newName = dialog.getText()
        if newName is None or len(newName.strip()) == 0 or newName == self.group.name:
            return

        from server.connection.ConnectionManager import connectionManager
        response = connectionManager.get().callRequest(GroupRequest.rename(self.group.id, newName))
        if response.isSuccessful():
            connectionManager.get().requestEarlyLoad()

    ##############################################################################
    def deleteGroup(self):
        dialog = CQuestionDialog("Are you sure?")
        if not dialog.show():
            return

        from server.connection.ConnectionManager import connectionManager
        response = connectionManager.get().callRequest(GroupRequest.delete(self.group.id))
        if response.isSuccessful():
            connectionManager.get().requestEarlyLoad()

