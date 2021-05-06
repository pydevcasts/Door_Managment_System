from common.kernel.setting.NumericSetting import NumericSetting


class PercentSetting(NumericSetting):

    def __init__(self, settingID, title, analyzerNo, receiveIndex, default, minValue, maxValue):
        NumericSetting.__init__(self, settingID, title, analyzerNo, receiveIndex, default, minValue, maxValue, "%")
