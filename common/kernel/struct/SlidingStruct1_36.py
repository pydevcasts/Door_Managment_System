from Lang import *
from common.kernel.core.BaseDataList import BaseDataList
from common.kernel.setting.FactoryReset import FactoryReset1
from common.kernel.setting.InitialSetup import InitialSetup1
from common.kernel.setting.ListSetting import ListSetting
from common.kernel.setting.MillimeterSetting import MillimeterSetting
from common.kernel.setting.NumericSetting import NumericSetting
from common.kernel.setting.OpenTime import OpenTime
from common.kernel.setting.PercentSetting import PercentSetting
from common.kernel.setting.SecondsSetting import SecondsSetting
from common.kernel.setting.SettingsPack import SettingsPack
from common.kernel.status.Sliding import slidingStatusList
from common.kernel.struct.AbstractStruct import MasterModel, AbstractStruct


class SlidingStruct1_36(AbstractStruct):

    ###################################################################################################################################
    def __init__(self):
        AbstractStruct.__init__(self)

    ###################################################################################################################################
    def getModel(self):
        return MasterModel.SLIDING

    ###################################################################################################################################
    def getVersion(self):
        return "1.36"

    ###################################################################################################################################
    def getDoorStatusList(self):
        return slidingStatusList

    ###################################################################################################################################
    def getInvalidImageAddress(self):
        return "images/sliding_invalid.png"

    ###################################################################################################################################
    def getMechanicalImageAddress(self):
        return "images/sliding_mechanical.png"

    ###################################################################################################################################
    def createSimpleSettings(self):
        simpleSettings = SettingsPack(SETTINGS)

        simpleSettings.add(PercentSetting(3010, OPEN_SPEED, 1500, 13, 100, 0, 100))
        simpleSettings.add(PercentSetting(3011, CLOSE_SPEED, 1500, 14, 50, 0, 100))
        simpleSettings.add(OpenTime())
        simpleSettings.add(PercentSetting(3013, PARTIAL_WIDTH, 1500, 16, 60, 30, 100))
        simpleSettings.add(MillimeterSetting(3015, MAX_OPEN_POINT, 1500, 22, 1, 0, 250))
        simpleSettings.add(SecondsSetting(3014, REMOTE_OPEN_TIME, 1500, 17, 3, 0, 99))
        simpleSettings.add(InitialSetup1())

        simpleSettings.add(ListSetting(3030, SENSOR_STYLE, 1500, 21, 0,
                                       BaseDataList({
                                           0: EUROPEAN,
                                           1: INTERNATIONAL,
                                           2: WITHOUT_SENSORS
                                       })
                                       ))

        simpleSettings.add(ListSetting(3040, RADAR_INSIDE, 1500, 19, 0,
                                       BaseDataList({
                                           0: NORMALLY_OPEN_NO,
                                           1: FREQUENCY_100HZ,
                                           2: CURRENT_MA_DC
                                       })
                                       ))

        return simpleSettings

    ###################################################################################################################################
    def createAdvancedSettings(self):
        advancedSettings = SettingsPack(ADVANCED_SETTINGS)

        advancedSettings.add(NumericSetting(3016, PUSH_IN_OPEN, 1500, 23, 0, 0, 30))

        advancedSettings.add(ListSetting(3017, MOTOR_DIRECTION, 1500, 24, 0,
                                         BaseDataList({
                                             0: NORMAL,
                                             1: INVERTED
                                         })
                                         ))

        advancedSettings.add(FactoryReset1())
        advancedSettings.add(NumericSetting(3018, AUTO_REVERSE, 1500, 25, 4, 1, 5))
        advancedSettings.add(NumericSetting(3019, AUTO_RESET_ERRORS, 1500, 26, 4, 0, 250, AUTO_RESET_ERRORS_POSTFIX))
        advancedSettings.add(ListSetting(3022, DOOR_ON_BATTERY, 1500, 27, 0,
                                         BaseDataList({
                                             0: NORMAL_OPERATON,
                                             1: STOP_IN_OPEN_POSITION
                                         })
                                         ))

        return advancedSettings
