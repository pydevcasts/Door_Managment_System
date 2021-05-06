from client.kernel.analyze.Analyzer1000 import analyzer1000
from client.kernel.core.CRC import crc
from client.kernel.core.SystemData import systemData
from client.kernel.serial.SerialSendQueue import serialSendQueue
from client.kernel.setting.SettingsManager import settingsManager


class SerialSendManager:

    ########################################################################
    def __init__(self):
        self.counter = 1

    ########################################################################
    def getCounter(self):
        c = self.counter
        self.counter = (self.counter + 1) % 0x100
        return c

    ########################################################################
    def Eigene_Sende_Kennung(self):
        return systemData.uc_Steuerung #کنترل

    ########################################################################
    def prepare(self, sendList):
        if sendList is None or len(sendList) < 9:
            return

        sendList[7] = self.Eigene_Sende_Kennung()
        sendList[9] = self.getCounter()
        crc.putCRC(sendList)

    ########################################################################
    def send(self, sendList):

        serialSendQueue.add(sendList)

        # Third priority, haven't we read the settings yet?
        # second priority, Some settings should be send, and then fetched the new value
        settingsManager.generateSendCommands()

        # First Priority, something exists in queue
        sendList = serialSendQueue.remove()

        # Fourt priority, simple door status
        if sendList is None:
            sendList = analyzer1000.generateStatusList()

        self.prepare(sendList)
        return sendList


#########################################
#########################################
#########################################
serialSendManager = SerialSendManager()
