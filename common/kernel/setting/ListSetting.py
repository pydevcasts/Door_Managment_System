from common.kernel.setting.Setting import Setting


class ListSetting(Setting):

    def __init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, baseDataList):
        self.baseDataList = baseDataList
        Setting.__init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault)

    def getDataList(self):
        return self.baseDataList

    def validate(self, value):
        return self.baseDataList.find(value) is not None

    def getTextForValue(self, value):
        baseData = self.baseDataList.find(value)
        if baseData is None:
            return ""
        return str(baseData)
