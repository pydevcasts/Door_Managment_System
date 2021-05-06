from client.kernel.Environment import environment
from common.kernel.Interface import Interface as commonKernelInterface


class Interface(commonKernelInterface):
    """
        [کرنل اینترفیس]: [لایه اینترفیس کل کرنله که اکسترن و شل با این لایه در ارتباطه
         و تو این داره کارهای اصلیمون انجام میشه ]
    Returns:
    متد استارت که بیرون هم استارت شد وقتی میگم استارت بشه یه فایلی بنام کامینیکیتور
    که همون نقشی و داره که سریال من و میسازه
    setting, handeling, addVersionListener,getDoorStatusList,addMechanicalListener,addSettingListener
    addDoorNameListener,addDoorErrorListener,addConfigurationsTo
    """
    #################################################################################
    def __init__(self):
        commonKernelInterface.__init__(self)

        from client.kernel.event.DoorErrorLogger import DoorErrorLogger
        from client.kernel.analyze.Analyzer1000 import analyzer1000
        analyzer1000.addDoorErrorListener(DoorErrorLogger())

    ######################################################################################
    def initialCheck(self):
        commonKernelInterface.initialCheck(self)
        """pyDes ‏این یک پیاده سازی پایتون خالص از الگوریتم رمزنگاری DES است. در پایتون خالص برای جلوگیری
         از مسائل قابل حمل است، چرا که بیشتر پیاده سازی های DES در C (به دلایل عملکرد) برنامه ریزی شده اند.‏"""

        try:
            import serial
        except:
            print("'PySerial' is not installed. install from https://pypi.python.org/pypi/pyserial/")
            import sys
            sys.exit()

    #################################################################################
    def start(self):
        commonKernelInterface.start(self)

        # start communication with serial Door
        from client.kernel.serial.SerialCommunicator import serialCommunicator
        serialCommunicator.start()  # start communication with serial Door

        # start IO Tasks
        from client.kernel.gpio.IOManager import ioManager
        ioManager.start()

    #################################################################################
    def waitForSettings(self, waitFlag):
        pass

    #################################################################################
    def setSettingMode(self, mode):
        from client.kernel.setting.SettingsManager import settingsManager
        settingsManager.settingMode = mode

    #################################################################################
    def isSerialConnected(self):
        from client.kernel.serial.SerialCommunicator import serialCommunicator
        return serialCommunicator.isSerialConnected()

    #################################################################################
    def getDoorStatusList(self):
        return environment.getDoorStatus().getDoorStatusList()

    #################################################################################
    def getSettings(self):
        return environment.getSettings()

    #################################################################################
    def handle(self, request, **kwargs):
        from client.kernel.handler.HandlerFactory import handlerFactory
        return handlerFactory.handle(request, **kwargs)
        """ isSerialConnected"""
    #################################################################################
    def addVersionListener(self, listener):
        environment.addVersionListener(listener)

    #################################################################################
    def addStatusListener(self, listener):
        doorStatus = environment.getDoorStatus()
        doorStatus.addStatusListener(listener)
        doorStatus.fireStatusChanged()

    #################################################################################
    def addSettingListener(self, listener):
        if listener is None:
            return
        from client.kernel.setting.SettingsManager import settingsManager
        settingsManager.addSettingListener(listener)

    #################################################################################
    def addMechanicalListener(self, listener):
        from client.kernel.serial.SerialCommunicator import serialCommunicator
        return serialCommunicator.addMechanicalListener(listener)

    #################################################################################
    def addDoorNameListener(self, listener):
        from client.kernel.core.DoorInfo import doorInfo
        return doorInfo.addDoorNameListener(listener)

    #################################################################################
    def addDoorErrorListener(self, listener):
        from client.kernel.analyze.Analyzer1000 import analyzer1000
        analyzer1000.addDoorErrorListener(listener)

    #################################################################################
    def addConfigurationsTo(self, configHolder):

        from Lang import MODEL, VERSION, PROJECT_KEY, DOOR_NAME, SERIAL_NO
        from client.kernel.Environment import environment
        configHolder.addConfig(MODEL, environment.getModel)  # read only
        configHolder.addConfig(VERSION, environment.getVersion)  # read only

        from client.kernel.core.DoorInfo import doorInfo
        configHolder.addConfig(PROJECT_KEY, doorInfo.getProject, doorInfo.setProject)
        configHolder.addConfig(DOOR_NAME, doorInfo.getName, doorInfo.setName)
        configHolder.addConfig(SERIAL_NO, doorInfo.getSerial)  # read only
