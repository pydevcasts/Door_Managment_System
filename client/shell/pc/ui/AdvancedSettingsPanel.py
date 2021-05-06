from client.shell.pc.PasswordManager import passwordManager
from client.shell.pc.setting.SettingsManager import settingsManager
from client.shell.pc.ui.SettingsPanel import SettingsPanel


class AdvancedSettingsPanel(SettingsPanel):

    ########################################################################
    def __init__(self):
        SettingsPanel.__init__(self)

    ########################################################################
    def access(self):
        return passwordManager.installerAccess()

    ########################################################################
    def activate(self):
        return settingsManager.activateAdvanced(self) > 0


########################################################################
########################################################################
########################################################################
advancedSettingsPanel = AdvancedSettingsPanel()
