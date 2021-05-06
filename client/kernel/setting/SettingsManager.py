import threading
import time
import traceback

from Globals import logger
from client.kernel.Environment import environment
from client.kernel.analyze.AnalyzerFactory import analyzerFactory


class SettingsManager:
    NOT_FOUND = "NOT FOUND"

    #################################################################################################
    def __init__(self):
        self.lock = threading.Lock()

        self.settingMode = False
        self.bufferedValues = {}
        self.logValues = {}

        # initialized, but not prepared
        self.simpleSettings = None
        self.advancedSettings = None
        self.settingList = []  # A type of cache
        self.simpleSettingList = []  # A type of cache
        self.advancedSettingList = []  # A type of cache
        self.settingMap = {}  # Another type of cache
        self.settingListeners = []

        environment.addVersionListener(self)

    #################################################################################################
    def versionFound(self, model, version):

        self.lock.acquire()

        try:
            self.simpleSettings, self.advancedSettings = environment.get().getSettings()

            # A type of cache
            self.simpleSettingList = []
            self.simpleSettingList.extend(self.simpleSettings.getPureSettingsList())

            self.advancedSettingList = []
            self.advancedSettingList.extend(self.advancedSettings.getPureSettingsList())

            self.settingList = []
            self.settingList.extend(self.simpleSettingList)
            self.settingList.extend(self.advancedSettingList)

            # Another type of cache
            self.settingMap = {}
            for setting in self.settingList:
                self.settingMap[setting.getParameterCode()] = setting
                tupple = (setting.getAnalyzerNo(), setting.getReceiveIndex())
                self.settingMap[tupple] = setting

            analyzers = environment.get().getAnalyzers()
            from client.kernel.analyze.AnalyzerFactory import analyzerFactory
            for analyzer in analyzers:
                analyzerFactory.register(analyzer)

        except:
            logger.exception(traceback.format_exc())

        self.lock.release()

        return True

    #################################################################################################
    def getSetting(self, key):
        if self.settingMap.get(key, None) is None:
            self.settingMap[key] = SettingsManager.NOT_FOUND

        if self.settingMap[key] == SettingsManager.NOT_FOUND:
            return None

        return self.settingMap[key]

    #################################################################################################
    def send(self, paramNo, value, sleepSeconds=1):

        setting = self.getSetting(paramNo)
        if setting is None:
            return -1, -1

        self.lock.acquire()

        if setting.getValue() is value:
            self.bufferedValues.pop(setting, None)
            self.lock.release()
            return paramNo, value

        if not setting.validate(value):
            self.lock.release()
            return paramNo, setting.getValue()

        self.bufferedValues[setting] = setting.serialize(value)

        self.lock.release()

        time.sleep(sleepSeconds)
        value = setting.getValue()
        return paramNo, value

    #################################################################################################
    def receiveAll(self, analyzerNo, dataList):
        for index in range(13, len(dataList)):
            tupple = (analyzerNo, index)
            setting = self.getSetting(tupple)
            if setting is None:
                continue

            serializedValue = 0
            valueLength = setting.getValueLength()
            for i in reversed(range(0, valueLength)):
                serializedValue = (serializedValue * 256) + dataList[index + i]

            self.receive(setting, serializedValue)

    #################################################################################################
    def receive(self, setting, serializedValue):

        value = setting.deserialize(serializedValue)
        if self.logValues.get(setting.getParameterCode(), None) == serializedValue:
            self.logValues.pop(setting.getParameterCode(), None)  # remove this value
            from Lang import SETTING_CHANGED_TO
            logger.success(SETTING_CHANGED_TO, setting.getTitle(), setting.getTextForValue(value))

        if setting.setValue(value):
            self.fireSettingChanged(setting.getParameterCode(), setting.getValue())

    #################################################################################################
    def generateSendCommands(self):
        from client.kernel.serial.SerialSendQueue import serialSendQueue

        analyzerSet = set()
        analyzerSet.update(analyzerFactory.getInvalidMap())  #

        try:
            self.lock.acquire()
            tempBufferedValues = self.bufferedValues.copy()
            self.bufferedValues.clear()
            self.lock.release()

            for setting, bufferedValue in tempBufferedValues.items():
                serialSendQueue.add(self.generateSettingNewVaue(setting, bufferedValue))

                logger.debug(
                    "Trying to send (" +
                    setting.getTextForValue(setting.deserialize(bufferedValue)) +
                    ") for \"" +
                    setting.getTitle() +
                    "\" parameter."
                    )
                self.logValues[setting.getParameterCode()] = bufferedValue
                analyzerSet.add(setting.getAnalyzerNo())

            tempBufferedValues.clear()

            for analyzerNo in analyzerSet:
                analyzer = analyzerFactory.get(analyzerNo)
                serialSendQueue.add(analyzer.generateSettingsRequest())
        except:
            logger.exception(traceback.format_exc())

        # serialSendQueue.commitBatch()
        # time.sleep(0.5)

    #################################################################################################
    def generateSettingNewVaue(self, setting, bufferedValue):
        if setting is None:
            return None

        analyzer = analyzerFactory.get(setting.getAnalyzerNo())
        return analyzer.generateSettingsNewVaue(setting.getParameterCode(), bufferedValue, setting.getValueLength())

    #################################################################################################
    def addSettingListener(self, listener):
        if listener is None:
            return
        self.settingListeners.append(listener)
        for setting in self.settingList:
            listener.settingChanged(setting.getParameterCode(), setting.getValue())  #

    #################################################################################################
    def fireSettingChanged(self, parameterCode, value):
        for listener in self.settingListeners:
            listener.settingChanged(parameterCode, value)

    #################################################################################################
    def invalidate(self):
        analyzerFactory.invalidate()

    #################################################################################################
    def isValid(self):
        return analyzerFactory.isValid()


###################################################
###################################################
###################################################
settingsManager = SettingsManager()
