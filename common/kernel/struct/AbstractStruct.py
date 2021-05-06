
class MasterModel:
    DUMMY =   "DUMMYM"

    SLIDING =   "0SLM0"
    FOLDING =   "0SLMF"
    REVOLVING = "0SLMR"
    SWING =     "0SLMS"

    models = [SLIDING, FOLDING, REVOLVING, SWING]


class AbstractStruct:

    ############################################################################
    def __init__(self):
        self.simpleSettings = self.createSimpleSettings()
        self.advancedSettings = self.createAdvancedSettings()

    ############################################################################
    def getModel(self) :
        return None

    ############################################################################
    def getVersion(self) :
        return 0.00

    ############################################################################
    def getModelVersion(self) :
        return self.getModel(), self.getVersion()

    ############################################################################
    def getDoorStatusList(self):
        return None

    ############################################################################
    def getOpenStatus(self):
        statusList = self.getDoorStatusList()
        if statusList is None:
            return None
        for status in statusList:
            if status.is_open_status:
                return status
        return None

    ############################################################################
    def getLockedStatus(self):
        statusList = self.getDoorStatusList()
        if statusList is None:
            return None
        for status in statusList:
            if status.is_locked_status:
                return status
        return None

    ############################################################################
    def getSettings(self):
        return self.simpleSettings, self.advancedSettings

    ############################################################################
    def createSimpleSettings(self):
        return None

    ############################################################################
    def createAdvancedSettings(self):
        return None
