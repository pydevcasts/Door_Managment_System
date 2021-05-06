from common.kernel.setting.NumericSetting import NumericSetting


class MillimeterSetting(NumericSetting):

    def __init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, minValue, maxValue):
        NumericSetting.__init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, minValue, maxValue,
                                " mm")
