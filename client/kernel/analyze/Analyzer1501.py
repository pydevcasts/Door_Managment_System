from client.kernel.analyze.Analyzer1500 import Analyzer1500

class Analyzer1501(Analyzer1500):

    ####################################################################################################
    def __init__(self):
        Analyzer1500.__init__(self)

    ####################################################################################################
    def getParamNo(self):
        return 1501 # 5-221

    ####################################################################################################
    def getSendParamNo(self):
        # Parameter-Nr = 3501 (13-173)
        return 3501

    ####################################################################################################
    def generateSettingsNewVaue(self, parameterNo, value, valueLength):
        dataList = Analyzer1500.generateSettingsNewVaue(self, parameterNo, value, valueLength + 1) #TODO why??
        return dataList
