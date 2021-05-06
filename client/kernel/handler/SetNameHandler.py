from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.SetNameResponse import SetNameResponse


class SetNameHandler(HandlerA):

    ###############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ###############################################################################
    def disconnectHandling(self):
        return True

    ###############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_OWNER
        return ROLE_OWNER

    ###############################################################################
    def handle(self, request, **kwargs):
        from client.kernel.core.DoorInfo import doorInfo

        if request.name is None or str(request.name).strip() == '':
            return SetNameResponse(doorInfo.getName(), False)

        accepted = doorInfo.setName(request.name)
        response = SetNameResponse(doorInfo.getName(), accepted)
        return response

    ###############################################################################
    def createEventLog(self, request, response):

        from client.kernel.event.EventLog import EventLog
        eventLog = EventLog(request, response)

        doorName = request.name

        eventLog.title = 'Door name Changed'
        eventLog.description = 'Door name has been changed to [' + doorName + "]."
        eventLog.param1 = doorName

        return eventLog


#######################################################
#######################################################
#######################################################
setNameHandler = SetNameHandler()
