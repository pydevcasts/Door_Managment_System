import time

from client.kernel.analyze.Analyzer1000 import analyzer1000
from client.kernel.core.Constants import Constants
from client.kernel.core.SystemData import systemData
from client.kernel.setting.CommandImpl import CommandImpl
from client.kernel.setting.SettingsManager import settingsManager


################################################################################
################################################################################
class FactoryResetImpl(CommandImpl):

    ############################################################################
    def __init__(self):
        CommandImpl.__init__(self)
        self.success = None
        self.value = None
        self.state = None

        ########################################################################

    def getParameterCode(self):
        return 3021

    ############################################################################
    def getModelVersion(self):
        from common.kernel.struct.AbstractStruct import MasterModel
        return MasterModel.SLIDING, "1.00"

    ############################################################################
    def execute(self, request):

        self.success = None
        self.value = 0
        self.state = 0
        systemData.currentState = Constants.MENUE_FACTORY_RESET
        analyzer1000.setCommand(self)

        while self.success is None:
            time.sleep(0.5)

        systemData.currentState = Constants.RUHEN
        result = self.success
        self.success = None
        return result

    ############################################################################
    def analyze(self, dataList):

        # case 0 :
        if self.state == 0:
            self.value = 1
            self.state = 1

        # case 1 :
        elif self.state == 1:
            self.value = 128  # 0x80
            self.state = 2

        # case 2 :
        elif self.state == 2:
            self.value = 2
            if self.shouldPerform():  # Door performs factory reset ?
                self.state = 3

        # case 3 :
        elif self.state == 3:
            self.value = 1
            if self.isPerformed():
                self.state = 4

        # case 4 :
        elif self.state == 4:
            analyzer1000.resetCommand()
            settingsManager.invalidate()
            self.success = True
            self.state = None

    ############################################################################
    def shouldPerform(self):
        return analyzer1000.machineStateMvD == 110

    ############################################################################
    def isPerformed(self):
        return \
            analyzer1000.machineStateMvD == 10 or \
            analyzer1000.machineStateMvD == 100

    ############################################################################
    def generateStatusList(self, sendList):

        if self.state is None:
            return sendList

        parameterCode = self.getParameterCode()
        sendList[10] = parameterCode // 256
        sendList[11] = parameterCode % 256

        sendList[1] = 16
        sendList.append(self.value)
        return sendList


################################################################################
################################################################################
class FactoryResetImpl2(FactoryResetImpl):

    ############################################################################
    def __init__(self):
        FactoryResetImpl.__init__(self)

    ############################################################################
    def getModelVersion(self):
        from common.kernel.struct.AbstractStruct import MasterModel
        return MasterModel.SLIDING, "2.00"

    ############################################################################
    def shouldPerform(self):
        return analyzer1000.machineStateMvD == Constants.state_systemReset

    ############################################################################
    def isPerformed(self):
        return \
            analyzer1000.machineStateMvD == Constants.state_close or \
            analyzer1000.machineStateMvD == Constants.state_open or \
            analyzer1000.machineStateMvD == Constants.state_driveToOpen or \
            analyzer1000.machineStateMvD == Constants.state_driveToClose or \
            analyzer1000.machineStateMvD == Constants.state_locked or \
            analyzer1000.machineStateMvD == Constants.state_startup


################################################################################
################################################################################
################################################################################
factoryResetImpl1 = FactoryResetImpl()
factoryResetImpl2 = FactoryResetImpl2()
