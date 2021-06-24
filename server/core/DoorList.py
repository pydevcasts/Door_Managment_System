import json
import threading

from Lang import lget, UNGROUPED_DOORS
from common.kernel.request.Response import Response
from server.core.Door import Door
from server.core.DoorGroup import DoorGroup


class DoorList:

    ###############################################################################
    def __init__(self):

        self.defaultGroup = DoorGroup(0, lget(UNGROUPED_DOORS))
        self.groupList = []

        self.listeners = []

        self.counter = 0
        self.delta = 2
        self.max = 10 * self.delta

        self.lock = threading.Lock()

    ###############################################################################
    def addListener(self, doorListListener):
        if (doorListListener is None) or (doorListListener in self.listeners):
            return
        self.listeners.append(doorListListener)

    ###############################################################################
    def removeListener(self, doorListListener):
        if (doorListListener is not None) and (doorListListener in self.listeners):
            self.listeners.remove(doorListListener)

    ###############################################################################
    def notify(self):
        for listener in self.listeners:
            listener.doorListChanged()

    ###############################################################################
    def getDoorGroupList(self):
        return [self.defaultGroup] + self.groupList

    ###############################################################################
    def findGroup(self, id_):
        if id_ == 0:
            return self.defaultGroup

        for group in self.groupList:
            if group.id == id_:
                return group

        return None

    ###############################################################################
    def findDoor(self, serial):
        door = self.defaultGroup.findDoor(serial)
        if door is not None:
            return door

        for group in self.groupList:
            door = group.findDoor(serial)
            if door is not None:
                return door

        return None

    ###############################################################################
    def clear(self):
        self.lock.acquire()
        for group in self.groupList:
            group.clear()
        self.groupList = []
        self.defaultGroup.clear()
        self.notify()
        self.lock.release()

    ###############################################################################
    def _insert(self, doorI, connectionInfo):
        if doorI is None:
            return

        result = False
        door = self.findDoor(doorI.serial)
        if door is None:
            result = True
            door = Door(doorI, connectionInfo)
            door.group = 0
            self.defaultGroup.insert(door)

        oldGroup = door.group
        newGroup = 0
        if hasattr(doorI, "group") and self.findGroup(doorI.group) is not None:
            newGroup = doorI.group
        if newGroup != oldGroup:
            self.findGroup(oldGroup).remove(door.serial)
            self.findGroup(newGroup).insert(door)
            result = True

        result = door.update(doorI) or result

        door.counter = self.counter
        return result

    ###############################################################################
    def insert(self, doorI, connectionInfo=None):
        self.lock.acquire()
        try:
            result = self._insert(doorI, connectionInfo)
            if result:
                self.notify()
            return result
        finally:
            self.lock.release()

    ###############################################################################
    def insertInfosResponse(self, infosResponse, connectionInfo=None):
        self.lock.acquire()

        try:
            result = False

            groupsIds = {0}
            for g in infosResponse.groups:
                id = g['id']
                name = g['name']
                groupsIds.add(id)
                group = self.findGroup(id)
                if group is None:
                    group = DoorGroup(id, name)
                    group.role = infosResponse.role
                    self.groupList.append(group)
                    result = True
                else:
                    result = group.rename(name) or result

            self.defaultGroup.role = infosResponse.role

            doorIs = []
            for info in infosResponse.infos:
                infoResponse = Response(0, json.dumps(info))
                doorIs.append(infoResponse)

            for doorI in doorIs:
                result = self._insert(doorI, connectionInfo) or result

            for i in reversed(range(0, len(self.groupList))):
                id = self.groupList[i].id
                if id not in groupsIds:
                    self.groupList = self.groupList[:i] + self.groupList[i+1:]

            if result:
                self.notify()
            return result

        finally:
            self.lock.release()

    ######################################## #######################################
    def changeStatus(self, serial, status):
        door = self.findDoor(serial)
        if door is None:
            return

        if door.status == status:
            return

        door.status = status
        self.notify()

    ###############################################################################
    def changeConnectionStatus(self, serial, connectionStatus):
        door = self.findDoor(serial)
        if door is None:
            return

        if door.connectionStatus == connectionStatus:
            return

        door.connectionStatus = connectionStatus
        self.notify()

    ###############################################################################
    def progress(self):

        self.lock.acquire()

        self.counter += 1
        self.counter %= self.max

        if self.cleansingRequired():
            if self.cleanseDoors():
                self.notify()

        self.lock.release()

    ###############################################################################
    def cleansingRequired(self):
        return (self.counter % self.delta) == 0

    ###############################################################################
    def validate(self, doorCounter):
        return ((self.max + self.counter - doorCounter) % self.max) <= self.delta

    ###############################################################################
    def cleanseDoors(self):  # synchronized
        cleaned = False
        size = len(self.defaultGroup.doorList)
        for i in range(size - 1, -1, -1):
            if not self.validate(self.defaultGroup.doorList[i].counter):
                self.defaultGroup.doorList = self.defaultGroup.doorList[:i] + self.defaultGroup.doorList[i + 1:]
                cleaned = True
        return cleaned


###################################################################################
###################################################################################
###################################################################################
doorList = DoorList()
