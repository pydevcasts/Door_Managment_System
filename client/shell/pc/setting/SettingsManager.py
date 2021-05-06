from Globals import interface
from client.shell.pc.setting.WrapperFactory import wrapperFactory


class SettingsManager:

    ################################################################################
    def __init__(self):
        self.simpleSettings = None
        self.advancedSettings = None

    ################################################################################
    def settingChanged(self, parameterCode, value):
        wrappers = []
        if self.simpleSettings is not None:
            wrappers.extend(self.simpleSettings.findAll(parameterCode))
        if self.advancedSettings is not None:
            wrappers.extend(self.advancedSettings.findAll(parameterCode))
        for wrapper in wrappers:
            wrapper.setValue(value)

    ################################################################################
    def versionFound(self, model, version):
        simpleSettings, advancedSettings = interface.get().getSettings()
        self.simpleSettings = wrapperFactory.wrap(simpleSettings)
        self.advancedSettings = wrapperFactory.wrap(advancedSettings)

    ################################################################################
    def activateSimple(self, panel):
        if self.simpleSettings is None:
            return 0

        self.simpleSettings.activate(panel)
        return len(self.simpleSettings)

    ################################################################################
    def activateAdvanced(self, panel):
        if self.advancedSettings is None:
            return 0

        self.advancedSettings.activate(panel)
        return len(self.advancedSettings)


########################################################################
########################################################################
########################################################################
settingsManager = SettingsManager()
