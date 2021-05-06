from Globals import logger
from common.kernel.event.EventLogger import eventLogger


class HandlerFactory:

    ######################################################################################
    def __init__(self):
        self.handlerMap = {}

    ######################################################################################
    def register(self, requestID, handler):
        self.handlerMap[requestID] = handler

    ######################################################################################
    def handle(self, request, **kwargs):
        logger.shit("Request: " + request.toJson())

        handler = self.handlerMap.get(request.getID(), None)
        if handler is None:
            log = kwargs.get('log', True)
            if log:
                logger.debug("Error! a request with unknown ID : " + str(request.getID()))
            return None

        response = handler.execute(request, **kwargs)
        logger.shit("Response: " + response.toJson())

        self.handleEventLog(handler, request, response, **kwargs)

        return response

    ######################################################################################
    def handleEventLog(self, handler, request, response, **kwargs):
        if handler is None or request is None or response is None:
            return

        eventLog = handler.createEventLog(request, response)
        if eventLog is None:
            return

        eventLogger.add(eventLog)