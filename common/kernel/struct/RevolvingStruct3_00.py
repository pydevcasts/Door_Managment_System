from Lang import *
from common.kernel.core.BaseDataList import BaseDataList
from common.kernel.setting.FactoryReset import FactoryReset1
from common.kernel.setting.ListSetting import ListSetting
from common.kernel.setting.MillimeterSetting import MillimeterSetting
from common.kernel.setting.NumericSetting import NumericSetting
from common.kernel.setting.PercentSetting import PercentSetting
from common.kernel.setting.SettingsPack import SettingsPack
from common.kernel.setting.ToggleSetting import ToggleSetting
from common.kernel.status.Revolving import revolvingStatusList
from common.kernel.struct.AbstractStruct import MasterModel, AbstractStruct


class RevolvingStruct3_00(AbstractStruct):

    ###################################################################################################################################
    def __init__(self):
        AbstractStruct.__init__(self)

    ###################################################################################################################################
    def getModel(self):
        return MasterModel.REVOLVING

    ###################################################################################################################################
    def getVersion(self):
        return "3.00"

    ###################################################################################################################################
    def getDoorStatusList(self):
        return revolvingStatusList

    ###################################################################################################################################
    def getInvalidImageAddress(self):
        return "images/revolving_invalid.png"

    ###################################################################################################################################
    def getMechanicalImageAddress(self):
        return "images/revolving_mechanical.png"

    ###################################################################################################################################
    def createSimpleSettings(self):
        simpleSettings = SettingsPack(SETTINGS)

        doorDiameter = simpleSettings.add(MillimeterSetting(3013, DOOR_DIAMETER, 1500, 16, 3001, 500, 3800))
        doorDiameter.setValueLength(2)  # 2 bytes

        simpleSettings.add(ListSetting(3012, NUMBER_OF_LEAVES, 1500, 18, 1,
                                       BaseDataList({
                                           0: FOUR_LEAVES,
                                           1: THREE_LEAVES
                                       })
                                       ))

        simpleSettings.add(NumericSetting(3015, ACTIVE_SECTIONS_NORM, 1500, 22, 3, 2, 15))
        simpleSettings.add(NumericSetting(3014, ACTIVE_SECTIONS_DISABLED, 1500, 23, 6, 4, 20))
        simpleSettings.add(ToggleSetting(3030, SENSOR_INSIDE_EXIST, 1500, 20, 0))
        simpleSettings.add(PercentSetting(3010, FAST_SPEED, 1500, 13, 50, 1, 100))
        simpleSettings.add(PercentSetting(3011, SLOW_SPEED, 1500, 14, 50, 1, 100))
        # simpleSettings.add(Command(3020, INITIAL_SETUP, "images/initialize_setup.png")) #TODO Deatails
        # simpleSettings.add(Command(?, "Show Serial", "images/serial32.png"))
        simpleSettings.add(ToggleSetting(3096, PUSH_AND_GO, 1500, 28, 0))
        simpleSettings.add(PercentSetting(3018, REVERSE_SENSITIVITY, 1500, 27, 70, 0, 100))
        simpleSettings.add(FactoryReset1())
        simpleSettings.add(
            MillimeterSetting(3017, SHIFT_SECURITY_AREA, 1500, 24, 127, 0, 250))  # TODO -125 <> +125 - shift +127

        return simpleSettings

    ###################################################################################################################################
    def createAdvancedSettings(self):
        advancedSettings = SettingsPack(ADVANCED_SETTINGS)
        return advancedSettings
