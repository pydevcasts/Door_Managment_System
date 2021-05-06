from Lang import SECONDS
from common.kernel.setting.NumericSetting import NumericSetting


class SecondsSetting(NumericSetting):

    def __init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, minValue, maxValue):
        NumericSetting.__init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, minValue, maxValue, SECONDS)
