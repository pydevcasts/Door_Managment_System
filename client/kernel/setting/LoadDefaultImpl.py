from client.kernel.setting.CommandImpl import CommandImpl


class LoadDefaultImpl(CommandImpl):

    ################################################################################
    def __init__(self):
        CommandImpl.__init__(self)

    ################################################################################
    def getParameterCode(self):
        return 3094

    ################################################################################
    def execute(self, request):
        from client.kernel.analyze.Analyzer1000 import analyzer1000
        dataList = analyzer1000.generateStatusList()

        parameterCode = self.getParameterCode()

        dataList[10] = parameterCode // 256
        dataList[11] = parameterCode % 256

        dataList[1] = 16  # extend one more byte
        dataList.append(0)

        from client.kernel.serial.SerialSendQueue import serialSendQueue

        dataList[15] = 128
        for i in range(1, 15):
            serialSendQueue.addBatch(dataList)

        dataList[15] = 2
        for i in range(1, 15):
            serialSendQueue.addBatch(dataList)

        dataList[15] = 3
        for i in range(1, 15):
            serialSendQueue.addBatch(dataList)

        serialSendQueue.commitBatch()

        import time
        time.sleep(6)

        from client.kernel.setting.SettingsManager import settingsManager
        settingsManager.invalidate()

        while not settingsManager.isValid():
            time.sleep(1)

        return True


################################################################################
################################################################################
################################################################################
loadDefaultImpl = LoadDefaultImpl()
