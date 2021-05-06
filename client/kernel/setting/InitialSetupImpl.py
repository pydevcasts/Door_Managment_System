from Globals import SIMULATION_ENABLED
from client.kernel.analyze.Analyzer1000 import analyzer1000, Analyzer1000
from client.kernel.core.Constants import Constants
from client.kernel.core.SystemData import systemData
from client.kernel.setting.WizardImpl import WizardImpl
from common.kernel.setting.InitialSetup import InitialSetup
from common.kernel.setting.Wizard import Wizard


########################################################################################################
########################################################################################################
class InitialSetupImpl(WizardImpl):

    ####################################################################################################
    def __init__(self):
        WizardImpl.__init__(self)
        self.value = None

    ####################################################################################################
    def getParameterCode(self):
        return 3020

    ####################################################################################################
    def getModelVersion(self):
        from common.kernel.struct.AbstractStruct import MasterModel
        return MasterModel.SLIDING, "1.00"

    ####################################################################################################
    def setState(self, state):
        if state == Wizard.STATE_START:
            return self.start()

        if state == Wizard.STATE_CANCEL:
            return self.cancel()

        if state == InitialSetup.STATE_SCAN_START:
            return self.scan()

        return WizardImpl.setState(self, state)

    ####################################################################################################
    def start(self):
        if self.getState() != Wizard.STATE_CLOSE:
            return False

        self.clearBuffer()
        WizardImpl.start(self)
        systemData.currentState = Constants.MENUE_INITIAL_SETUP
        analyzer1000.setCommand(self)
        return True

    ####################################################################################################
    def scan(self):
        if self.getState() != InitialSetup.STATE_QUESTION_2:
            return False
        return self.setState_(InitialSetup.STATE_SCAN_START)

    ####################################################################################################
    def cancel(self):
        if self.getState() > InitialSetup.STATE_QUESTION_2:
            return False
        return WizardImpl.cancel(self)

    ####################################################################################################
    def finish(self, state):
        analyzer1000.resetCommand()
        systemData.currentState = Constants.RUHEN
        self.bufferState(state)
        self.setState_(Wizard.STATE_CLOSE)

    ####################################################################################################
    def analyze(self, dataList):

        # state = 0 : Full Open by Hand
        if self.state == Wizard.STATE_START:
            self.value = 1
            self.setState_(InitialSetup.STATE_QUESTION_1)

        # state = 1 : Door is full open ?
        elif self.state == InitialSetup.STATE_QUESTION_1:
            self.value = 1
            self.setState_(InitialSetup.STATE_QUESTION_2)

        # state = 2 : Start new Door scanning ? (Waiting for user to scan or cancel)
        elif self.state == InitialSetup.STATE_QUESTION_2:
            self.value = 1

        # state = 3 : Door scanning in process
        elif self.state == InitialSetup.STATE_SCAN_START:
            self.value = 2
            if self.isLearningStarted():
                self.setState_(InitialSetup.STATE_SCAN_PROCESS)

        # state = 4 : Door scanning in process
        elif self.state == InitialSetup.STATE_SCAN_PROCESS:
            self.value = 1
            if self.isLearningFinished():
                self.setState_(InitialSetup.STATE_SCAN_FINISH)

        # state = 5 : Learning completed
        elif self.state == InitialSetup.STATE_SCAN_FINISH:
            if self.isLearningFailed():
                self.setState_(InitialSetup.STATE_SCAN_FAIL)
            else:
                self.setState_(InitialSetup.STATE_SCAN_SUCCESS)

        # state = 6 : Learning was not OK!
        elif self.state == InitialSetup.STATE_SCAN_FAIL:
            self.finish(Wizard.STATE_FAIL)

        # state = 6 : Lerning was OK!
        elif self.state == InitialSetup.STATE_SCAN_SUCCESS:
            self.finish(Wizard.STATE_SUCCESS)

        # state = cancel
        elif self.state == Wizard.STATE_CANCEL:
            self.finish(Wizard.STATE_CANCEL)

    ####################################################################################################
    def isLearningStarted(self):
        return analyzer1000.machineStateMvD == 30

    ####################################################################################################
    def isLearningFinished(self):
        return analyzer1000.machineStateMvD == 10 or analyzer1000.machineStateMvD == 100

    ####################################################################################################
    def isLearningFailed(self):
        return analyzer1000.position == 31999 or analyzer1000.position == 32000

    ####################################################################################################
    def generateStatusList(self, sendList):

        sendList[1] = 16
        sendList[10] = 11
        sendList[11] = 204  # Parameter-Nr = 3020
        sendList.append(self.value)  # sendList[15] = setupValue

        return sendList


########################################################################################################
########################################################################################################
class InitialSetupImpl2(InitialSetupImpl):

    ####################################################################################################
    def __init__(self):
        InitialSetupImpl.__init__(self)

    ####################################################################################################
    def getModelVersion(self):
        from common.kernel.struct.AbstractStruct import MasterModel
        return MasterModel.SLIDING, "2.00"

    ####################################################################################################
    def isLearningStarted(self):
        return analyzer1000.machineStateMvD == Constants.state_learning

    ####################################################################################################
    def isLearningFinished(self):
        error = analyzer1000.getSystemError(Analyzer1000.DEF_STAND_ALONE)
        return error == 0 or error >= 12


########################################################################################################
########################################################################################################
class InitialSetupImplDummy(InitialSetupImpl):

    ####################################################################################################
    def __init__(self):
        InitialSetupImpl.__init__(self)
        self.scanCounter = 0

    ####################################################################################################
    def start(self):
        if self.getState() != Wizard.STATE_CLOSE:
            return False

        self.clearBuffer()
        WizardImpl.start(self)
        systemData.currentState = Constants.MENUE_INITIAL_SETUP

        import threading
        threading.Thread(target=self.simulate).start()  # , args=[response.requests]

        return True

    ####################################################################################################
    def finish(self, state):
        systemData.currentState = Constants.RUHEN
        self.bufferState(state)
        self.setState_(Wizard.STATE_CLOSE)

    ####################################################################################################
    def simulate(self):

        self.scanCounter = 100
        while self.getState() != Wizard.STATE_CLOSE:
            import time
            time.sleep(0.1)
            self.analyze(None)

    ####################################################################################################
    def isLearningStarted(self):
        return True

    ####################################################################################################
    def isLearningFinished(self):
        self.scanCounter -= 1
        return self.scanCounter <= 0

    ####################################################################################################
    def isLearningFailed(self):
        import random
        return random.random() >= 0.75


########################################################################################################
########################################################################################################
########################################################################################################
initialSetupImplDummy = None
initialSetupImpl1 = None
initialSetupImpl2 = None

if SIMULATION_ENABLED:
    initialSetupImplDummy = InitialSetupImplDummy()
else:
    initialSetupImpl1 = InitialSetupImpl()
    initialSetupImpl2 = InitialSetupImpl2()
