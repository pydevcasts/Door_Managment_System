from Globals import logger, ini


# from common.kernel.status.Sliding import slidingStatusList

#####################################################################
#####################################################################
# Status_Parameter_ID = 2000


#####################################################################
#####################################################################
class DoorStatus:
    # We made this static, to be shared between all instances of DoorStatus.
    statusListeners = []

    ################################################################################
    def __init__(self, statusList):
        self.value = None
        self.statusList = statusList

        self.setValue(self.getDefaultValue())

    ################################################################################
    def getDoorStatusList(self):
        return self.statusList

    ################################################################################
    """??????????"""
    def getDefault(self):
        for status in self.statusList:
            if status.default:
                return status.key

        return self.statusList[0].key

    ################################################################################
    def getDefaultValue(self):
        status = ini.getDoorStatus()
        """????????"""""
        logger.debug("DoorData.init - ini.getDoorStatus() = " + str(status))
        if self.validate(status):
            return status
        return self.getDefault()

    ################################################################################
    def getSettingModeValue(self):
        for status in self.statusList:
            if status.settingMode:
                """?????"""
                return status.key

        return self.getDefault()

    ################################################################################
    def validate(self, value):
        return self.statusList.find(value) is not None

    ################################################################################
    def getValue(self):
        return self.value

    ################################################################################
    def set_Value(self, value):

        if self.value == value:
            return False

        if not self.validate(value):
            return False

        self.value = value
        self.fireStatusChanged()
        return True

    ################################################################################
    def setValue(self, value):
        if not self.set_Value(value):
            return False
        from Lang import DOOR_STATUS_CHANGED_TO
        logger.info(DOOR_STATUS_CHANGED_TO, self.statusList.find(value))
        ini.setDoorStatus(value)
        ini.save()

    ################################################################################
    def addStatusListener(self, listener):
        if listener is None:
            return
        DoorStatus.statusListeners.append(listener)
        listener.statusChanged(self.value)
        """?????statusChanged"""

    ################################################################################
    def fireStatusChanged(self):
        for listener in DoorStatus.statusListeners:
            listener.statusChanged(self.value)
