from client.kernel.analyze.AnalyzerA import AnalyzerA

class Analyzer1500(AnalyzerA):

    ####################################################################################################
    def __init__(self):
        AnalyzerA.__init__(self)
        self.valid_ = False
        self.waiting = 0

    ####################################################################################################
    def getParamNo(self):
        return 1500 # 5-220

    ####################################################################################################
    def getSendParamNo(self):
        # Parameter-Nr = 3500 (13-172)
        return 3500

    ####################################################################################################
    def analyze(self, dataList):

        from Globals import interface
        interface.get().waitForSettings(True)

        self.valid_ = True
        self.waiting = 0

        from client.kernel.setting.SettingsManager import settingsManager
        settingsManager.receiveAll(self.getParamNo(), dataList)

        interface.get().waitForSettings(False)

        return None

    ####################################################################################################
    def generateSettingsRequest(self):

        from client.kernel.analyze.Analyzer1000 import analyzer1000
        dataList = analyzer1000.generateStatusList()

        p = self.getSendParamNo()
        dataList[10] = p // 256
        dataList[11] = p % 256

        return dataList

    ####################################################################################################
    def generateSettingsNewVaue(self, parameterNo, value, valueLength):

        from client.kernel.analyze.Analyzer1000 import analyzer1000
        dataList = analyzer1000.generateStatusList()

        dataList[10] = parameterNo // 256
        dataList[11] = parameterNo % 256

        for i in range(0, valueLength):
            dataList[1] += 1 #extend one more byte
            dataList.append(value % 256)
            value = value // 256

        return dataList

    ####################################################################################################
    def isValid(self):
        return self.valid_

    ####################################################################################################
    def setValid(self, valid):
        self.valid_ = valid

    ####################################################################################################
    def checkForValidity(self):
        if self.valid_:
            return True

        self.waiting = self.waiting + 1

        if self.waiting <= 1:
            return False

        if self.waiting < 8:
            return True

        self.waiting = 0
        return False
