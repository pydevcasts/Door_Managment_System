from Globals import logger
from client.kernel.handler.HandlerA import HandlerA
from client.kernel.setting.SettingsManager import settingsManager
from common.kernel.request.SetParamResponse import SetParamResponse


class SetParamHandler(HandlerA):

    ############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ############################################################################
    def getAccessRole(self, request):
        from client.kernel.Environment import environment
        simple, advanced = environment.getSettings()

        from common.kernel.core.Role import ROLE_OWNER, ROLE_INSTALLER

        if simple.find(request.code) is not None:
            return ROLE_OWNER

        return ROLE_INSTALLER

    ############################################################################
    def handle(self, request, **kwargs):
        try:
            code = request.code
            value = request.value
            code, value = settingsManager.send(code, value)
        except:
            import traceback
            logger.exception(traceback.format_exc())
            code = -1
            value = -1

        return SetParamResponse(code, value)

    ###############################################################################
    def createEventLog(self, request, response):

        from client.kernel.event.EventLog import EventLog
        eventLog = EventLog(request, response)

        code = request.code
        value = request.value

        from client.kernel.setting.SettingsManager import settingsManager
        setting = settingsManager.getSetting(code)

        from Lang import lgetDefault
        title = lgetDefault(setting.title)
        eventLog.title = title + ' Changed'
        eventLog.description = title + ' has been changed to [' + setting.getTextForValue(value) + "]."
        eventLog.param1 = code
        eventLog.param2 = value

        return eventLog


#######################################################
#######################################################
#######################################################

setParamHandler = SetParamHandler()
