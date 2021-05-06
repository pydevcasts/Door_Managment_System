from client.kernel.analyze.Analyzer1000 import analyzer1000
from client.kernel.analyze.AnalyzerA import AnalyzerA


class Analyzer1503(AnalyzerA):

    ####################################################################################################
    def __init__(self):
        AnalyzerA.__init__(self)

    ####################################################################################################
    def getParamNo(self):
        return 1503 # 5-223

    ####################################################################################################
    def getSendParamNo(self):
        # Parameter-Nr = 3501 (13-173)
        return 3503

    ####################################################################################################
    def generateSerialNoRequest(self):

        dataList = analyzer1000.generateStatusList()

        p = self.getSendParamNo()
        dataList[10] = p // 256
        dataList[11] = p % 256

        return dataList

    ####################################################################################################
    def analyze(self, dataList):
        serialNo = ""
        for i in range(13, 21) :
            serialNo += chr(dataList[i])

        from client.kernel.core.DoorInfo import doorInfo
        doorInfo.setSerial(serialNo)

###############################################################
###############################################################
###############################################################

analyzer1503 = Analyzer1503()
