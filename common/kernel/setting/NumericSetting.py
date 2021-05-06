from Lang import lget
from common.kernel.setting.Setting import Setting


class NumericSetting(Setting):
    """ پدر همه ستینگزهای عددی هستش"""

    def __init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, minValue, maxValue, textPostfix=""):
        Setting.__init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault)
        self.minValue = minValue
        self.maxValue = maxValue
        self.textPostfix = textPostfix
        """ چه پسوندیه که دیفالتش خالیه"""

    ################################################################################
    def getDefaultValue(self):
        return -1

    ################################################################################
    def validate(self, value):
        return (value >= self.minValue) and (value <= self.maxValue)

    ################################################################################
    def getTextForValue(self, value):
        return str(value) + lget(self.textPostfix)
