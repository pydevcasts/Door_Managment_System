from Lang import lget


class Setting:

    def __init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault):
        self.value = self.getDefaultValue()
        self.settingID = settingID
        self.title = title
        self.analyzerNo = analyzerNo
        self.receiveIndex = receiveIndex
        self.factoryDefault = factoryDefault

        self.valueLength = 1  # number of bytes used in value

    ################################################################################
    def getParameterCode(self):
        return self.settingID

    ################################################################################
    def getTitle(self):
        return lget(self.title)

    ################################################################################
    def getAnalyzerNo(self):
        return self.analyzerNo

    ################################################################################
    def getReceiveIndex(self):
        return self.receiveIndex

    ################################################################################
    def getDefaultValue(self):
        return None

    ################################################################################
    def getFactoryDefault(self):
        return self.factoryDefault

    ################################################################################
    def find(self, code):
        if self.settingID == code:
            return self
        return None

    ################################################################################
    def getPureSettingsList(self):
        return [self]

    ################################################################################
    def getTextForValue(self, value):
        if value is None:
            return ""
        return str(value)

    ################################################################################
    def getValueText(self):
        return self.getTextForValue(self.getValue())

    ################################################################################
    def validate(self, value):
        return True

    ################################################################################
    def getValue(self):
        return self.value

    ################################################################################
    def setValue(self, value):
        if value is self.getValue():
            return False
        if not self.validate(value):
            return False
        self.updateValue(value)
        return True

    ################################################################################
    def updateValue(self, value):
        self.value = value

    ################################################################################
    def serialize(self, value):  # Proper value to send via serial line
        return value

    ################################################################################
    def deserialize(self, value):  # change the value received from serial line to app value
        return value

    ################################################################################
    def getValueLength(self):
        return self.valueLength

    ################################################################################
    def setValueLength(self, valueLength):
        self.valueLength = valueLength
