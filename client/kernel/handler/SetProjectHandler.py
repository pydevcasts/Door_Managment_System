from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.SetProjectResponse import SetProjectResponse


class SetProjectHandler(HandlerA):

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
        from client.kernel.core.DoorInfo import doorInfo
        doorInfo.setProject(request.newProject)
        return SetProjectResponse(True)


#######################################################
#######################################################
#######################################################

setProjectHandler = SetProjectHandler()
