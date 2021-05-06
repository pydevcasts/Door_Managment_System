import time

from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.SskResponse import SskResponse


class SskHandler(HandlerA):

    ###############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ###############################################################################
    def disconnectHandling(self):
        return True

    ###############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_ADVANCED_USER
        return ROLE_ADVANCED_USER

    ###############################################################################
    def handle(self, request, **kwargs):

        from Globals import SIMULATION_ENABLED
        if SIMULATION_ENABLED:
            time.sleep(1.5)
            return SskResponse(True)

        try:
            import RPi.GPIO as GPIO

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(8, GPIO.OUT)

            GPIO.output(8, GPIO.HIGH)
            time.sleep(1.5)
            GPIO.output(8, GPIO.LOW)

            return SskResponse(True)
        except:
            return SskResponse(False)

    ###############################################################################
    def createEventLog(self, request, response):

        from client.kernel.event.EventLog import EventLog
        eventLog = EventLog(request, response)
        eventLog.title = 'SSK Activated'
        eventLog.description = 'SSK Activated on the door.'
        return eventLog


#######################################################
#######################################################
#######################################################

sskHandler = SskHandler()
