from client.kernel.setting.CommandImpl import CommandImpl


################################################################################
################################################################################
class ChangeSerialImpl1(CommandImpl):

    ################################################################################
    def __init__(self):
        CommandImpl.__init__(self)

    ################################################################################
    def getParameterCode(self):
        return 3095

    ################################################################################
    def execute(self, request):
        pass

    ############################################################################
    def requestDoorSerial(self):
        from common.kernel.lsc.Hardware import getSystemSerial
        serialNo = getSystemSerial()
        while serialNo[0] == '0':
            serialNo = serialNo[1:]
        serialNo = (serialNo + "-9876543210")[:8]

        return serialNo


################################################################################
################################################################################
class ChangeSerialImpl2(ChangeSerialImpl1):

    ############################################################################
    def __init__(self):
        ChangeSerialImpl1.__init__(self)

    ############################################################################
    def getModelVersion(self):
        from common.kernel.struct.AbstractStruct import MasterModel
        return MasterModel.SLIDING, "2.00"

    ############################################################################
    """
    def requestDoorSerial(self):
        from client.kernel.analyze.AnalyzerFactory import analyzerFactory
        from client.kernel.serial.SerialSendQueue import serialSendQueue
        analyzer = analyzerFactory.get(1503)
        serialSendQueue.add(analyzer.generateSerialNoRequest())
        import time
        time.sleep(0.5)
    """

    ############################################################################
    def execute(self, request):

        serialNo = str(request.serial)

        if len(serialNo) != 8:
            return False

        from client.kernel.analyze.Analyzer1000 import analyzer1000
        defaultList = analyzer1000.generateStatusList()

        parameterCode = self.getParameterCode()

        dataList = defaultList[:]  # create a copy
        dataList[10] = parameterCode // 256
        dataList[11] = parameterCode % 256

        dataList[1] = 17  # extend two more bytes
        dataList.append(0)
        dataList.append(0)

        from client.kernel.serial.SerialSendQueue import serialSendQueue
        for i in range(0, 7):
            if ord(serialNo[i]) < ord('0') or ord(serialNo[i]) > ord('9'):
                serialSendQueue.rollbackBatch()
                return False

            dataList[15] = 50 + ord(serialNo[i]) - ord('0')
            dataList[16] = i
            serialSendQueue.addBatch(dataList)

            for j in range(1, 5):
                serialSendQueue.addBatch(defaultList)

        dataList[15] = 0
        dataList[16] = 8
        serialSendQueue.addBatch(dataList)

        serialSendQueue.commitBatch()

        import time
        time.sleep(7)

        return True


################################################################################
################################################################################
################################################################################
changeSerialImpl1 = ChangeSerialImpl1()
changeSerialImpl2 = ChangeSerialImpl2()
