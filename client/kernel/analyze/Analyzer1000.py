from client.kernel.Environment import environment
from client.kernel.analyze.AnalyzerA import AnalyzerA
from client.kernel.core.FaultManager import FaultManager
from client.kernel.core.SystemData import systemData


class Analyzer1000(AnalyzerA):
    # index definition for all quadratic variables:
    #وریبل درجه دوم
    DEF_STAND_ALONE = 0
    DEF_FRW_MASTER = 1
    DEF_FRW_SLAVE = 2
    DEF_PRG = 3

    ####################################################################################################
    def __init__(self):
        AnalyzerA.__init__(self)

        self.resetCommand()

        self.systemProgram = [0, 0, 0, environment.getDoorStatus()]  # uc_Programmart_System
        self.systemError = [0, 0, 0, 0]  # uc_Fehlerart_System
        self.machineState = [0, 0, 0, 0]  # uc_Automaten_Istzustand
        self.machineStateMvD = 0  # uc_Automaten_Istzustand_MvD
        self.position = 0  # si_IST_STRECKE_MvD

        self.masterPotentiometer1 = 0  # uc_Poti_Faktor_P1_Master
        self.masterPotentiometer2 = 0  # uc_Poti_Faktor_P2_Master
        self.masterPotentiometer3 = 0  # uc_Poti_Faktor_P3_Master
        # self.masterPartialOpen    = 0 # uc_Part_Open_Prozent_Master
        # self.masterRemoteOpenTime = 0 # uc_Remote_Open_Time_Master
        # self.masterPharmacyOpen   = 0 # uc_Pharmacy_Open_Prozent_Master

        self.errorList = []
        self.errorListeners = []
        self.error0start = 0

        self.lastPing = "[]"
        self.cycles = 0

    #################################################################################
    def addDoorErrorListener(self, listener):
        if listener is None:
            return

        self.errorListeners.append(listener)
        listener.updateDoorError(self.getSystemError(), self.now())

    ####################################################################################################
    def getParamNo(self):
        return 1000

    ####################################################################################################
    def setCommand(self, command):
        self.command = command

    ####################################################################################################
    def resetCommand(self):
        self.command = None

    ####################################################################################################
    def analyze(self, dataList):

        self.lastPing = str(dataList)

        systemType = dataList[7]

        self.systemProgram[systemType] = dataList[14]
        self.systemError[systemType] = dataList[13]
        self.machineState[systemType] = dataList[12]

        self.machineStateMvD = dataList[12]

        oldPosition = self.position
        self.position = dataList[15] * 256 + dataList[16]

        self.masterPotentiometer1 = dataList[17]
        self.masterPotentiometer2 = dataList[18]
        self.masterPotentiometer3 = dataList[19]

        if self.position < 2000 <= oldPosition:
            self.cycles += 1

        self.updateErrorList()

        if self.command is not None:
            self.command.analyze(dataList)

        # return generateStatusList()
        return None

    ####################################################################################################
    def generateStatusList(self):
        sendList = [128, 15, 0, 0, 100, 63, 112, 3, 80, 0, 11, 184, 10, 0, 2]

        sendList[0] = 0x80
        sendList[1] = 15
        sendList[4] = 0x64
        sendList[5] = 63  # 63 = '?'
        sendList[6] = 112  # 112 = 'p'
        # sendList[7] = Eigene_Sende_Kennung()
        sendList[8] = 0x50
        # sendList[9] = uc_Telegramm_Zaehler_Senden
        sendList[10] = 0x0B
        sendList[11] = 0xB8  # Parameter-Nr = 3000
        sendList[12] = systemData.currentState
        sendList[13] = FaultManager.uc_Fehlerart
        sendList[14] = self.getConditionalDoorStatus()

        if self.command is not None:
            sendList = self.command.generateStatusList(sendList)

        return sendList

    ####################################################################################################
    def getConditionalDoorStatus(self):
        doorStatus = environment.getDoorStatus()
        from client.kernel.setting.SettingsManager import settingsManager
        if settingsManager.settingMode:
            return doorStatus.getSettingModeValue()
        return doorStatus.getValue()

    ####################################################################################################
    def getSystemError(self, systemType=None):
        if systemType is not None:
            return self.systemError[systemType]

        indices = [Analyzer1000.DEF_PRG, Analyzer1000.DEF_STAND_ALONE, Analyzer1000.DEF_FRW_MASTER,
                   Analyzer1000.DEF_FRW_SLAVE]

        for index in indices:
            if self.systemError[index] > 0:
                return self.systemError[index]

        return 0

    ####################################################################################################
    def now(self):
        import time
        return int(round(time.time() * 1000))

    ####################################################################################################
    def updateErrorList(self):

        now = self.now()
        oldErrorCode = -1
        if len(self.errorList) > 0:
            oldErrorCode = self.errorList[0][0]

        errorCode = self.getSystemError()

        # the first entry
        if len(self.errorList) == 0:
            self.errorList.append((errorCode, now))
        # continuous error, extend the current
        elif self.errorList[0][0] == errorCode:
            self.errorList[0] = (errorCode, now)
        # debounce mode - remove the glitch zeros
        elif errorCode == 0:
            if self.error0start == 0:
                self.error0start = now
            elif now - self.error0start >= 2000:
                self.errorList = [(errorCode, now - 2000)] + self.errorList
                self.error0start = 0
        # we have a new error for sure
        else:
            self.errorList = [(errorCode, now)] + self.errorList
            self.error0start = 0

        index = len(self.errorList) - 1
        duration = 15 * 60 * 1000  # 15 minutes
        while index >= 0:
            if now - self.errorList[index][1] <= duration:
                break
            index -= 1

        if index == len(self.errorList) - 1:
            pass
        else:
            self.errorList = self.errorList[:index + 1]

        if oldErrorCode == self.errorList[0][0]:
            return

        for listener in self.errorListeners:
            listener.updateDoorError(self.errorList[0][0], self.errorList[0][1])

    ####################################################################################################
    def getRecentErrorList(self):

        if len(self.errorList) == 0:
            return []

        import time
        now = int(round(time.time() * 1000))

        result = []
        for errPair in self.errorList:
            if errPair[0] == 0:
                continue
            result.append((errPair[0], now - errPair[1]))

        return result

    ####################################################################################################
    def getLastPing(self):
        return self.lastPing

    ####################################################################################################
    def getCycles(self):
        return self.cycles


###############################################################
###############################################################
###############################################################
analyzer1000 = Analyzer1000()
