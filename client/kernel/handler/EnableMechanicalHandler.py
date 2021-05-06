import time

from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.EnableMechanicalResponse import EnableMechanicalResponse


class EnableMechanicalHandler(HandlerA):
    """ disconnectHandling, getAccessRole,createEventLog, DMS Enabled on the door,Mechanical switch Enabled on the door"""
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
        from client.kernel.serial.SerialCommunicator import serialCommunicator
        mechanical = serialCommunicator.setMechanical(request.mechanical)
        time.sleep(4)
        return EnableMechanicalResponse(mechanical)

    ###############################################################################
    def createEventLog(self, request, response):

        from client.kernel.event.EventLog import EventLog
        eventLog = EventLog(request, response)

        eventLog.title = 'Mechanical switch Enabled'
        eventLog.description = 'Mechanical switch Enabled on the door.'

        mechanical = request.mechanical
        if not mechanical:
            eventLog.title = 'DMS Enabled'
            eventLog.description = 'DMS Enabled on the door.'

        return eventLog


#######################################################
#######################################################
#######################################################

enableMechanicalHandler = EnableMechanicalHandler()
