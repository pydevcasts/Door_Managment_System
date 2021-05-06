from common.kernel.request.InfoResponse import InfoResponse


class Door:

    ###############################################################################
    def __init__(self, doorI, connectionInfo):

        self.serial = doorI.serial
        self.name = doorI.name

        self.connectionInfo = connectionInfo

        self.connectionStatus = doorI.connectionStatus
        self.status = doorI.status

        self.version = doorI.version
        self.model = doorI.model

        self.doorError = doorI.doorError

        self.group = 0
        try:
            self.group = int(doorI.group)
        except:
            pass

        self.params = {}
        try:
            self.params.update(doorI.params)
        except:
            pass

        self.properties = {}
        try:
            self.properties.update(doorI.properties)
        except:
            pass

        from common.kernel.Structure import structure
        self.struct = structure.get(self.model, self.version)

        self.password = None

        self.counter = -1

    ###############################################################################
    def __repr__(self):
        if self.name is not None and len(self.name) > 0:
            return self.name
        return "<" + self.serial + ">"

    ###############################################################################
    def isConnectionValid(self):
        return self.connectionStatus != InfoResponse.CONNECTION_STATUS_INVALID

    ###############################################################################
    def isDigital(self):
        return self.connectionStatus == InfoResponse.CONNECTION_STATUS_DIGITAL

    ###############################################################################
    def isMechanical(self):
        return self.connectionStatus == InfoResponse.CONNECTION_STATUS_MECHANICAL

    ###############################################################################
    def update(self, doorI):  # doorI : door or infoResponse or DoorResponse

        if doorI is None:
            return False

        result = (self.serial != doorI.serial)
        self.serial = doorI.serial

        result = result or (self.connectionStatus != doorI.connectionStatus)
        self.connectionStatus = doorI.connectionStatus

        result = result or (self.name != doorI.name)
        self.name = doorI.name

        result = result or (self.status != doorI.status)
        self.status = doorI.status

        result = result or (self.doorError != doorI.doorError)
        self.doorError = doorI.doorError

        newGroup = 0
        if hasattr(doorI, "group") and doorI.group is not None:
            newGroup = doorI.group
        result = result or (self.group != newGroup)
        self.group = newGroup

        try:
            self.params.update(doorI.params)
        except:
            pass

        try:
            self.properties.update(doorI.properties)
        except:
            pass

        return result

    ###############################################################################
    def getStructure(self):
        from common.kernel.Structure import structure
        return structure.get(self.model, self.version)

    ###############################################################################
    def getStatusList(self):
        structure = self.getStructure()
        return structure.getDoorStatusList()

    ###############################################################################
    def getStatus(self):
        statusList = self.getStatusList()
        return statusList.find(self.status)

    ###############################################################################
    def isInOpenStatus(self):
        return self.getStructure().getOpenStatus() == self.getStatus()

    ###############################################################################
    def isInLockedStatus(self):
        return self.getStructure().getLockedStatus() == self.getStatus()

    ###############################################################################
    def getImageAddress(self):

        if not self.isConnectionValid():
            return self.struct.getInvalidImageAddress()

        if self.isMechanical():
            return self.struct.getMechanicalImageAddress()

        status = self.getStatus()
        return status.imageAddress

    ###############################################################################
    def getErrorImageAddress(self):
        from common.kernel.core.DoorErrors import doorErrors
        return doorErrors.getImageAddress(self.doorError)

    ###############################################################################
    def isBlocked(self):
        return self.doorError == 130

    ###############################################################################
    def isManipulated(self):
        return self.doorError == 142 and self.properties.get("position", 0) > 500
