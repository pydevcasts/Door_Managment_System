from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.SetWebServerResponse import SetWebServerResponse


class SetWebServerHandler(HandlerA):

    ###############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ###############################################################################
    def disconnectHandling(self):
        return True

    ###############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_INSTALLER
        return ROLE_INSTALLER

    ###############################################################################
    def handle(self, request, **kwargs):
        from client.extern.websocket.WebServerCommunicator import webServerCommunicator
        webServerCommunicator.setWebServerUrl(request.webServer)
        return SetWebServerResponse(True)


#######################################################
#######################################################
#######################################################

setWebServerHandler = SetWebServerHandler()
