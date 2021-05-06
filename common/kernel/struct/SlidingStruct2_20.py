from Lang import *
from common.kernel.core.BaseDataList import BaseDataList
from common.kernel.setting.ChangeSerial import ChangeSerial
from common.kernel.setting.FactoryReset import FactoryReset2
from common.kernel.setting.InitialSetup import InitialSetup2
from common.kernel.setting.ListSetting import ListSetting
from common.kernel.setting.LoadDefaults import LoadDefaults
from common.kernel.setting.MillimeterSetting import MillimeterSetting
from common.kernel.setting.NumericSetting import NumericSetting
from common.kernel.setting.OpenTime import OpenTime
from common.kernel.setting.PercentSetting import PercentSetting
from common.kernel.setting.SaveDefaults import SaveDefaults
from common.kernel.setting.SecondsSetting import SecondsSetting
from common.kernel.setting.SettingsPack import SettingsPack
from common.kernel.setting.ToggleSetting import ToggleSetting
from common.kernel.struct.SlidingStruct1_36 import SlidingStruct1_36


class SlidingStruct2_20(SlidingStruct1_36):
    """ در با این مشخصه"""  
    ###################################################################################################################################
    def __init__(self):
        SlidingStruct1_36.__init__(self)

    ###################################################################################################################################
    def getVersion(self):
        return "2.20"

    ###################################################################################################################################
    def createSimpleSettings(self):
        simpleSettings = SettingsPack(SETTINGS)
        """ اومدیم ستینگز و تعریف کردیم"""
        self.openSpeed = simpleSettings.add(PercentSetting(3010, OPEN_SPEED, 1500, 13, 95, 0, 100))
        """ من یه ستینگزی دارم که مقدارش درصدهکه یونیک ای دیش 3010 هستش
         و تو انالایزر 1500 خونده میشه و ایندکس 13 ام ارایه 1500ماست  
         دیفالت ولیوش 95 هستش که از 0 تا 100 میتونه تغییر بکنه
        """
        self.closeSpeed = simpleSettings.add(PercentSetting(3011, CLOSE_SPEED, 1500, 14, 70, 0, 100))
        simpleSettings.add(OpenTime())
        simpleSettings.add(PercentSetting(3013, PARTIAL_WIDTH, 1500, 16, 60, 5, 80))
        simpleSettings.add(MillimeterSetting(3015, MAX_OPEN_POINT, 1500, 22, 12, 0, 250))
        simpleSettings.add(SecondsSetting(3014, REMOTE_OPEN_TIME, 1500, 17, 5, 0, 99))

        # simpleSettings.add(LockType())
        simpleSettings.add(ListSetting(3017, MOTOR_DIRECTION, 1500, 24, 0,
                                       BaseDataList({
                                           0: NORMAL,
                                           1: INVERTED
                                       })
                                       ))
        simpleSettings.add(ListSetting(3030, SENSOR_STYLE, 1500, 21, 1,
                                       BaseDataList({
                                           0: EUROPEAN,
                                           1: INTERNATIONAL
                                       })
                                       ))

        simpleSettings.add(InitialSetup2())
        simpleSettings.add(LoadDefaults())

        inputFunctionList = BaseDataList({
            0: NO_FUNCTION_NO,
            1: FORCE_OP_NO,
            2: FORCE_TO_CL_NO,
            3: STAY_SHUTDOWN_NO,
            4: SIDE_SCAN_NO,
            5: FLIP_FLOP_NO,
            10: NO_FUNCTION_NC,
            11: FORCE_OP_NC,
            12: FORCE_TO_CL_NC,
            13: STAY_SHUTDOWN_NC,
            14: SIDE_SCAN_NC,
            15: FLIP_FLOP_NC
        })

        inputFunctions = simpleSettings.add(SettingsPack(INPUT_FUNCTIONS))
        inputFunctions.add(ListSetting(3097, STOP, 1501, 26, 0, inputFunctionList))
        inputFunctions.add(ListSetting(3098, ESCAPE, 1501, 25, 0, inputFunctionList))
        inputFunctions.add(ListSetting(3099, REMOTE, 1501, 27, 1, inputFunctionList))

        return simpleSettings

    ###################################################################################################################################
    def createAdvancedSettings(self):
        advancedSettings = SettingsPack(ADVANCED_SETTINGS)

        advancedSettings.add(PercentSetting(3018, AUTO_REVERSE, 1500, 25, 50, 0, 100))
        advancedSettings.add(SecondsSetting(3019, AUTO_RESET_ERRORS, 1500, 26, 30, 0, 250))
        advancedSettings.add(ListSetting(3022, DOOR_ON_BATTERY, 1500, 27, 0,
                                         BaseDataList({
                                             0: NORMAL_OPERATON,
                                             1: STOP_IN_OPEN_POSITION
                                         })
                                         ))
        advancedSettings.add(NumericSetting(3023, SET_BATTERY_VOLTAGE, 1500, 28, 220, 180, 220, " V/10"))

        advancedSettings.add(FactoryReset2())
        advancedSettings.add(SaveDefaults())

        setRamps = advancedSettings.add(SettingsPack(SET_RAMPS))

        openRamps = setRamps.add(SettingsPack(OPEN_RAMPS))
        openRamps.add(PercentSetting(3062, ACCELERATION_SLOPE, 1501, 13, 85, 10, 100))
        openRamps.add(PercentSetting(3063, DECELERATION_SLOPE, 1501, 14, 45, 10, 101))
        openRamps.add(self.openSpeed)
        openRamps.add(PercentSetting(3064, SLOW_SPEED, 1501, 15, 25, 0, 100))
        openRamps.add(MillimeterSetting(3065, SLOW_SPEED_START_POINT, 1501, 16, 43, 0, 250))
        openRamps.add(MillimeterSetting(3066, MINIMUM_SPEED_START_POINT, 1501, 17, 4, 0, 250))

        closeRamps = setRamps.add(SettingsPack(CLOSE_RAMPS))
        closeRamps.add(PercentSetting(3067, ACCELERATION_SLOPE, 1501, 18, 50, 10, 100))
        closeRamps.add(PercentSetting(3068, DECELERATION_SLOPE, 1501, 19, 35, 10, 101))
        closeRamps.add(self.closeSpeed)
        closeRamps.add(PercentSetting(3069, SLOW_SPEED, 1501, 20, 8, 0, 100))
        closeRamps.add(MillimeterSetting(3070, SLOW_SPEED_START_POINT, 1501, 21, 28, 0, 250))
        closeRamps.add(MillimeterSetting(3071, MINIMUM_SPEED_START_POINT, 1501, 22, 0, 0, 250))

        # setRamps.add(AccelMotionProfile())
        # setRamps.add(DecelMotionProfile())

        motorValues = advancedSettings.add(SettingsPack(SET_MOTOR_VALUES))
        motorValues.add(MillimeterSetting(3060, PULLY_SIZE, 1504, 13, 60, 1, 250))
        motorValues.add(NumericSetting(3061, GEARBOX_REDUCTION, 1504, 14, 15, 1, 90, ":1"))
        motorValues.add(NumericSetting(3059, ENCODER_PULSES, 1504, 15, 100, 1, 250, ENCODER_PULSES_VALUE_POSTFIX))
        motorValues.add(PercentSetting(3072, MOTOR_VOLTAGE, 1504, 16, 95, 10, 99))
        motorValues.add(NumericSetting(3073, GLOBAL_MINIMUM_SPEED, 1504, 17, 50, 1, 250, " mm/s"))

        behavior = advancedSettings.add(SettingsPack(BEHAVIOR))
        behavior.add(ToggleSetting(3081, POSITION_CONTROL_CLOSE_ONE_WAY, 1502, 14, 0))
        behavior.add(ToggleSetting(3082, POSITION_CONTROL_OPEN_PARTIAL, 1502, 15, 0))
        behavior.add(ListSetting(3084, AFTER_AUTO_REVERSE_IN_OPEN_DIRECTION, 1502, 17, 1,
                                 BaseDataList({
                                     1: OPEN_AFTER_3_SECONDS,
                                     2: OPEN_AFTER_6_SECONDS,
                                     0: CLOSE
                                 })
                                 ))
        behavior.add(ListSetting(3085, AFTER_AUTO_REVERSE_IN_CLOSE_DIRECTION, 1502, 18, 1,
                                 BaseDataList({
                                     1: OPEN_AND_WAIT_2X,
                                     2: OPEN_AND_WAIT_3X,
                                     0: OPEN
                                 })
                                 ))
        behavior.add(ListSetting(3086, ONE_WAY_TRAFFIC, 1502, 19, 0,
                                 BaseDataList({
                                     0: EXIT_ONLY,
                                     1: ENTRY_ONLY
                                 })
                                 ))
        behavior.add(NumericSetting(3087, HIGH_TRAFFIC_VALUE, 1502, 20, 20, 1, 250))
        behavior.add(NumericSetting(3088, HIGH_TRAFFIC_BEHAVIOUR, 1502, 21, 10, 1, 250))
        behavior.add(ToggleSetting(3089, TWO_WAY_TRAFFIC, 1502, 22, 0))
        behavior.add(ToggleSetting(3090, LOCK_CHECK, 1502, 23, 1))
        behavior.add(ToggleSetting(3092, OPEN_BY_FORCE, 1502, 25, 1))

        manufacturerSettings = advancedSettings.add(SettingsPack(MANUFACTURER_SETTINGS))
        manufacturerSettings.add(ChangeSerial())
        manufacturerSettings.add(ListSetting(3040, RADAR_INSIDE, 1500, 19, 0,
                                             BaseDataList({
                                                 0: NORMALLY_OPEN_NO,
                                                 1: FREQUENCY_100HZ,
                                                 2: CURRENT_MA_DC
                                             })
                                             ))

        return advancedSettings
