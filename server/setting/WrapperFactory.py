from common.kernel.setting.ChangeSerial import ChangeSerial
from common.kernel.setting.Command import Command
from common.kernel.setting.InitialSetup import InitialSetup
from common.kernel.setting.Setting import Setting
from common.kernel.setting.SettingsPack import SettingsPack
from common.shell.setting.SettingsPackWrapper import SettingsPackWrapper
from server.connection.ConnectionManager import connectionManager
from server.setting.CommandWrapper import CommandWrapper
from server.setting.InitialSetupWrapper import InitialSetupWrapper
from server.setting.SettingWrapper import SettingWrapper


class WrapperFactory:

    def __init__(self):
        pass

    def wrap(self, setting, parentWrapper=None, doorPanel=None):

        web = connectionManager.get().getConnectionType() == connectionManager.CONNECTION_TYPE_WEB

        if web and isinstance(setting, Command):
            return None

        if isinstance(setting, InitialSetup):
            return InitialSetupWrapper(setting, doorPanel)  # TODO implement for 2

        if isinstance(setting, ChangeSerial):
            return None  # TODO implement

        if isinstance(setting, Command):
            commandWrapper = CommandWrapper(setting, doorPanel)
            return commandWrapper

        if isinstance(setting, SettingsPack):
            return SettingsPackWrapper(self, setting, parentWrapper, doorPanel=doorPanel)

        if isinstance(setting, Setting):
            settingWrapper = SettingWrapper(setting, doorPanel)
            return settingWrapper

        return None


########################################################
########################################################
########################################################
wrapperFactory = WrapperFactory()
