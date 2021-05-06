from client.kernel.setting.CommandImpl import CommandImpl


class SaveDefaultImpl(CommandImpl):

    ################################################################################
    def __init__(self):
        CommandImpl.__init__(self)

    ################################################################################
    def getParameterCode(self):
        return 3093

    ################################################################################
    def execute(self, request):
        from client.kernel.analyze.Analyzer1000 import analyzer1000
        dataList = analyzer1000.generateStatusList()

        parameterCode = self.getParameterCode()

        dataList[10] = parameterCode // 256
        dataList[11] = parameterCode % 256

        dataList[1] = 16  # extend one more byte
        dataList.append(3)

        from client.kernel.serial.SerialSendQueue import serialSendQueue
        for i in range(1, 40):
            serialSendQueue.addBatch(dataList)
        serialSendQueue.commitBatch()

        import time
        time.sleep(6)

        return True


################################################################################
################################################################################
################################################################################
saveDefaultImpl = SaveDefaultImpl()
