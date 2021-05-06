from common.kernel.setting.SecondsSetting import SecondsSetting


class OpenTime(SecondsSetting):

    def __init__(self):
        SecondsSetting.__init__(self, 3012, 'Open Time', 1500, 15, 1, 0, 20)

    ################################################################################
    def serialize(self, value):  # Proper value to send via serial line
        return value * 5

    ################################################################################
    def deserialize(self, value):  # change the value received from serial line to app value
        return value // 5
