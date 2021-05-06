from Globals import logger
from client.kernel.handler.HandlerA import HandlerA
from client.kernel.setting.SettingsManager import settingsManager
from common.kernel.request.SetParamsResponse import SetParamsResponse


class SetParamsHandler(HandlerA):

    ############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_OWNER
        return ROLE_OWNER

    ############################################################################
    def handle(self, request, **kwargs):
        result = {}
        try:
            for code, value in request.params.items():
                try:
                    settingsManager.send(code, value, sleepSeconds=0.3)
                except:
                    pass
        except:
            import traceback
            logger.exception(traceback.format_exc())
            result = {}

        import time
        time.sleep(2)

        from common.kernel.request.DoorRequest import DoorRequest
        from client.kernel.handler.DoorHandler import doorHandler
        response = doorHandler.handle(DoorRequest())

        for code, value in response.params.items():
            result[code] = value

        return SetParamsResponse(result)


#######################################################
#######################################################
#######################################################

setParamsHandler = SetParamsHandler()
