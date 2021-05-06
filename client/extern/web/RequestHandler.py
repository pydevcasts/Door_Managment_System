import web
from Globals import logger


class RequestHandler:
    """authentication about request
    """
    def GET(self):
        inputt = web.input(_method='get')

        requestStr = inputt['request']

        logger.shit("Received via web service: " + requestStr)

        from common.kernel.request.Request import Request
        request = Request(Request.UNDEFINED, requestStr)

        from Globals import interface
        response = interface.get().handle(request)

        return response.toJson()
