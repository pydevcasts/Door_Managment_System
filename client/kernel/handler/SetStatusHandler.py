from client.kernel.Environment import environment
from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.SetStatusResponse import SetStatusResponse


class SetStatusHandler(HandlerA):

    ###############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ###############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_USER
        return ROLE_USER

    ###############################################################################
    def handle(self, request, **kwargs):
        """  میاد از ابجکت ریکویست مقدار استتوسشو میخون و با مقدار استتوسی که تو 
        environment  
        مون هستش مقایسه میکنه و ست میکنه و رسپانش..."""
        status = request.status
        if status <= 0:
            return None

        doorStatus = environment.getDoorStatus()
        doorStatus.setValue(status)
        return SetStatusResponse(doorStatus.getValue())

    ###############################################################################
    def createEventLog(self, request, response):
        from client.kernel.event.EventLog import EventLog
        eventLog = EventLog(request, response)

        doorStatus = environment.getDoorStatus()

        eventLog.title = 'Status Changed'
        eventLog.description = 'Door Status has been changed to ' + str(doorStatus.statusList.find(request.status)) + "."
        eventLog.param1 = request.status

        return eventLog


#######################################################
#######################################################
#######################################################

setStatusHandler = SetStatusHandler()
