
class DoorGroup:
    ###############################################################################
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.role = -1
        self.doorList = []

    ###############################################################################
    def __repr__(self):
        return self.name

    ###############################################################################
    def getDoorList(self):
        return self.doorList

    ###############################################################################
    def rename(self, name):
        if name is None or name == self.name:
            return False
        self.name = name
        return True

    ###############################################################################
    def clear(self):
        self.doorList = []

    ###############################################################################
    def findDoor(self, serial):
        for door in self.doorList:
            if door.serial == serial:
                return door
        return None

    ###############################################################################
    def insert(self, door):
        if door is None or self.findDoor(door.serial):
            return
        self.doorList.append(door)

    ###############################################################################
    def remove(self, serial):
        for i in range(0, len(self.doorList)):
            door = self.doorList[i]
            if door.serial == serial:
                self.doorList = self.doorList[:i] + self.doorList[i+1:]
                return door
        return None
