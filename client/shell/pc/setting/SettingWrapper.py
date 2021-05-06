from Globals import interface
from common.shell.setting.SettingWrapper import SettingWrapper as CommonSettingWrapper


class SettingWrapper(CommonSettingWrapper):

    ################################################################################
    def __init__(self, setting):
        CommonSettingWrapper.__init__(self, setting)

    ################################################################################
    def onNewValueAccepted(self, value):

        parameterCode = self.setting.getParameterCode()

        from common.kernel.request.SetParamRequest import SetParamRequest
        request = SetParamRequest(parameterCode, value)

        from client.shell.pc.PasswordManager import passwordManager
        passwordManager.fillRequest(request)

        interface.get().handle(request)
