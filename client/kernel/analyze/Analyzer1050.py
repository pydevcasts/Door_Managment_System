from client.kernel.Environment import environment
from client.kernel.analyze.AnalyzerA import AnalyzerA
from client.kernel.core.OrganizationData import organizationData

class Analyzer1050(AnalyzerA):

    ####################################################################################################
    def __init__(self):
        AnalyzerA.__init__(self)

    ####################################################################################################
    def getParamNo(self):
        return 1050

    ####################################################################################################
    def analyze(self, dataList):

        environment.updateVersion(dataList)

        sendList = [
                0x80,
                24,   # Length
                0,    # CRC - high
                0,    # CRC - Low
                0x64,
                ord('?'),
                ord('p'),
                0,    # will be set
                0x50,
                0,    # Counter - Will be set
                0x0B, # Param No = 3050 - High
                0xEA, # Param No = 3050 - Low
            ]

        sendList += organizationData.uc_Steuerungstype[:]
        sendList += organizationData.uc_SW_Version[:]

        return sendList

####################################################################################################
####################################################################################################
####################################################################################################
analyzer1050 = Analyzer1050()
