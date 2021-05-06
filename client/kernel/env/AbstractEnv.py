from client.kernel.status.DoorStatus import DoorStatus
from common.kernel.struct.AbstractStruct import AbstractStruct


class AbstractEnv(AbstractStruct):
    """createDoorStatus,getAnalyzers,createAnalyzers
    """
    ############################################################################
    def __init__(self):
        AbstractStruct.__init__(self)
        self.doorStatus = self.createDoorStatus()
        self.analyzers = self.createAnalyzers()

    ############################################################################
    def getDoorStatus(self):
        return self.doorStatus

    ############################################################################
    def getAnalyzers(self):
        return self.analyzers

    ############################################################################
    def createDoorStatus(self):
        return DoorStatus(self.getDoorStatusList())

    ############################################################################
    def createAnalyzers(self):
        return []
