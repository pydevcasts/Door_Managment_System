from common.shell.setting.SettingWrapper import SettingWrapper as CommonSettingWrapper


class SettingWrapper(CommonSettingWrapper):

    ################################################################################
    def __init__(self, setting, doorPanel):
        CommonSettingWrapper.__init__(self, setting)
        """shell, PyQT, Ui
        """
        self.doorPanel = doorPanel

    ################################################################################
    def onNewValueAccepted(self, value):

        parameterCode = self.setting.getParameterCode()
        """initialized in settingwrapper
        """
        from common.kernel.request.SetParamRequest import SetParamRequest
        request = SetParamRequest(parameterCode, value)
        response, exception = self.doorPanel.callRequest(request)

        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        if response.isBuffered():
            # TODO a waiting mechanism
            self.doorPanel.alert("It might take a few seconds")
            return

        self.doorPanel.setSettingValue(parameterCode, response.value)
