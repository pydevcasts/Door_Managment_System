from PyQtImports import QWidget, QGridLayout, QVBoxLayout, QMetaObject, pyqtSignal
from common.shell.ui.UI import mainComponentBorder, grayBackground
from server.core.DoorList import doorList
from server.ui.list.GroupListWidgetItem import GroupListWidgetItem


class GroupListWidget(QWidget):
    doorListChangedSignal = pyqtSignal()
    selectSignal = pyqtSignal(str)

    #############################################################################
    def __init__(self):
        QWidget.__init__(self)

        QMetaObject.connectSlotsByName(self)
        self.doorListChangedSignal.connect(self.doorListChangedSlot)
        self.selectSignal.connect(self.selectSlot)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        innerWidget = QWidget()
        innerWidget.setStyleSheet(mainComponentBorder() + grayBackground())
        layout.addWidget(innerWidget, 0, 0, 1, 1)

        self.layout = QVBoxLayout(innerWidget)

        doorList.addListener(self)

        self.selectedDoorItemValidator = None

    ############################################################
    def setSelectedDoorItemValidator(self, selectedDoorItemValidator):
        self.selectedDoorItemValidator = selectedDoorItemValidator

    ############################################################
    def validateSelectedDoorItem(self, doorItem):
        if doorItem is None:
            self.clearSelection()
        return self.selectedDoorItemValidator is None or self.selectedDoorItemValidator.validateSelectedDoorItem(doorItem)

    #############################################################################
    def onGroupItemClicked(self, groupItem):
        if groupItem is None:
            return
        self.expandOn(groupItem.group.id)

    #############################################################################
    def expandOn(self, groupId):
        for index in range(0, self.layout.count()):
            groupItem = self.layout.itemAt(index).widget()
            if groupItem.group.id == groupId:
                self.layout.setStretch(index, 1)
            else:
                self.layout.setStretch(index, 0)
            groupItem.expandOn(groupId)

    #############################################################################
    def onDoorItemClicked(self, doorListWidgetItem):
        if doorListWidgetItem is None:
            return

        door = doorListWidgetItem.door

        if not self.validateSelectedDoorItem(door):
            return

        serial = door.serial
        self.select(serial)

    #############################################################################
    def clearSelection(self):
        self.select("")

    #############################################################################
    def select(self, serial):
        self.selectSignal.emit(serial)

    #############################################################################
    def selectSlot(self, serial):
        for index in range(0, self.layout.count()):
            self.layout.itemAt(index).widget().selectOn(serial)

    #############################################################################
    def doorListChanged(self):
        self.doorListChangedSignal.emit()

    #############################################################################
    def doorListChangedSlot(self):

        groupList = doorList.getDoorGroupList()

        groupMap = {}
        for group in groupList:
            groupMap[group.id] = group

        removeArr = []

        for index in range(0, self.layout.count()):

            groupItem = self.layout.itemAt(index).widget()
            id = groupItem.group.id
            if id not in groupMap:
                removeArr = [groupItem] + removeArr
                continue

            groupItem.updateUI(groupMap.pop(id, None))

        # remove items which are not existing any more
        for groupItem in removeArr:
            if groupItem.expanded:
                self.expandOn(0)
            self.layout.removeWidget(groupItem)
            groupItem.setParent(None)

        # add the remaining items in doorMap, these are the new doors
        for group in groupMap.values():
            groupItem = GroupListWidgetItem(group, self)
            stretch = 0
            if self.layout.count() == 0:
                stretch = 1
            self.layout.addWidget(groupItem, stretch)

        self.layout.itemAt(0).widget().setHeaderVisible(self.layout.count() > 1)
