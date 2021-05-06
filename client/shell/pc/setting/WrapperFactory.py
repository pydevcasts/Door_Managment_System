from client.shell.pc.setting.ChangeSerialWrapper import ChangeSerialWrapper
from client.shell.pc.setting.CommandWrapper import CommandWrapper
from client.shell.pc.setting.InitialSetupWrapper import InitialSetupWrapper
from client.shell.pc.setting.SettingWrapper import SettingWrapper
from common.kernel.setting.ChangeSerial import ChangeSerial
from common.kernel.setting.Command import Command
from common.kernel.setting.InitialSetup import InitialSetup
from common.kernel.setting.Setting import Setting
from common.kernel.setting.SettingsPack import SettingsPack
from common.shell.setting.SettingsPackWrapper import SettingsPackWrapper


class WrapperFactory:

    def __init__(self):
        pass

    def wrap(self, setting, parentWrapper=None):

        if isinstance(setting, InitialSetup):
            return InitialSetupWrapper(setting)

        if isinstance(setting, ChangeSerial):
            return ChangeSerialWrapper(setting)

        if isinstance(setting, Command):
            return CommandWrapper(setting)

        if isinstance(setting, SettingsPack):
            return SettingsPackWrapper(self, setting, parentWrapper)

        if isinstance(setting, Setting):
            return SettingWrapper(setting)

        return None


########################################################
########################################################
########################################################
wrapperFactory = WrapperFactory()
