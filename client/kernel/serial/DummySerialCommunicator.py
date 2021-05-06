import threading
import time

from client.kernel.analyze.AnalyzerFactory import analyzerFactory


################################################################################
################################################################################
class DummySerialCommunicator(threading.Thread):

    ############################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="DummySerialCommunicator")

        self.setDaemon(True)

        import random
        random.seed()

        from client.kernel.Environment import environment
        from common.kernel.struct.AbstractStruct import MasterModel
        environment.model = MasterModel.SLIDING
        environment.version = "1.38"
        environment.notifyVersionFound()

        #from client.kernel.core.DoorInfo import doorInfo
        #doorInfo.setSerial("simulated_serial1")

        from client.kernel.setting.SettingsManager import settingsManager
        for setting in settingsManager.settingList:
            setting.setValue(setting.factoryDefault)

        self.counter = 1
        self.connected = True
        self.reset()
        self.mechanical = False
        self.mechanicalListeners = []

        self.dummyErrorCounter = 0
        self.dummyError = 0

    ############################################################################
    def reset(self):
        self.sendList = None

        # settings value

        from client.kernel.setting.SettingsManager import settingsManager
        settingsManager.invalidate()

    ############################################################################
    def run(self):

        while True:
            time.sleep(1.0 / 8.0)
            self.handShake(not self.mechanical)

    ############################################################################
    def handShake(self, sendResponse=True):
        dataList = self.read()
        if dataList is None:
            return

        # p = dataList[10] * 256 + dataList[11]
        # if p != 1000 and p != 3000 :
        #    print("r: " + str(dataList))

        # print(dataList)
        from client.kernel.serial.SerialSendManager import serialSendManager
        sendList = analyzerFactory.analyze(dataList)

        if not sendResponse:
            return

        sendList = serialSendManager.send(sendList)
        self.send(sendList)
        # print(sendList)

        # p = sendList[10] * 256 + sendList[11]
        # if p != 1000 and p != 3000 :
        #    print("s: " + str(sendList))

    ############################################################################
    def read(self):
        time.sleep(1.0 / 8.0)
        dataList = self.generateDefaultList()

        if self.sendList is not None:
            dataList = self.answer(self.sendList)
            self.sendList = None

        dataList[9] = self.getCounter()

        from client.kernel.core.CRC import crc
        crc.putCRC(dataList)

        return dataList

    ############################################################################
    def send(self, sendList):
        self.sendList = sendList

    ############################################################################
    def generateDefaultList(self):
        dataList = [128, 20, 0, 0, 100, 63, 112, 3, 80, 0, 3, 232, 0, 0, 0, 0, 0, 0, 0, 0]
        dataList[13] = self.randomError()
        from client.kernel.Environment import environment
        dataList[14] = environment.getDoorStatus().getValue()

        return dataList

    ############################################################################
    def randomError(self):
        self.dummyErrorCounter -= 1
        if self.dummyErrorCounter <= 0:
            self.dummyErrorCounter = 100

            import random
            self.dummyError = random.choice([0, 0, 10, 0, 0, 0, 100, 0, 130, 142, 0, 0, 210, 0, 0, 0, 0, 240, 0, 0, 0])

        return self.dummyError

    ############################################################################
    def answer(self, sendList):

        paramCode = sendList[10] * 256 + sendList[11]

        # Handle analyzers
        try:
            from client.kernel.analyze.AnalyzerFactory import analyzerFactory
            analyzerFactory.get(paramCode - 2000).valid_ = True
        except:
            pass

        # Handle Settings
        try:
            from client.kernel.setting.SettingsManager import settingsManager
            setting = settingsManager.getSetting(paramCode)

            if setting is not None:

                index = 15
                value = 0
                while True:
                    try:
                        value = (value * 256) + sendList[index]
                        index = index + 1
                    except:
                        break

                settingsManager.receive(setting, value)

        except:
            pass

        return self.generateDefaultList()

    ############################################################################
    def getCounter(self):
        c = self.counter
        self.counter = (self.counter + 1) % 0x100
        return c

    ############################################################################
    def isSerialConnected(self):
        return not self.mechanical

    ############################################################################
    def setMechanical(self, mechanical):
        if self.mechanical == mechanical:
            return

        self.mechanical = mechanical
        self.fireMechanicalChanged()
        return self.mechanical

    ############################################################################
    def addMechanicalListener(self, listener):
        if listener is None:
            return
        self.mechanicalListeners.append(listener)

    ############################################################################
    def fireMechanicalChanged(self):
        for listener in self.mechanicalListeners:
            listener.mechanicalChanged(self.mechanical)
