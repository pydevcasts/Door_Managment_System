

class DoorErrorLogger:
    def __init__(self):
        pass

    def updateDoorError(self, errorCode, errorTime):

        if errorCode == 0:
            return

        from common.kernel.core.DoorErrors import doorErrors
        doorError = doorErrors.find(errorCode)

        from client.kernel.event.EventLog import EventLog
        eventLog = EventLog()
        eventLog.title = 'Door Error (%s)' % errorCode

        from Lang import lgetDefault
        eventLog.description = 'Door Error: %s' % lgetDefault(doorError.message)

        eventLog.door_error = errorCode
        eventLog.door_error_description = lgetDefault(doorError.message)

        from common.kernel.event.EventLogger import eventLogger
        eventLogger.add(eventLog)
