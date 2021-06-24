import web
from Globals import logger


class RequestHandler:
    """authentication about request
    """
    def GET(self):
        inputt = web.input(_method='get')
        """You now have your web.py application running a real web server on your computer.
            Visit that URL and you should see “Hello, world!” 
            (You can add an IP address/port after the “code.py” bit to control
        where web.py launches the server. You can also tell it to run a fastcgi or scgi server.)
        """
        requestStr = inputt['request']

        logger.shit("Received via web service: " + requestStr)

        from common.kernel.request.Request import Request
        request = Request(Request.UNDEFINED, requestStr)

        from Globals import interface
        response = interface.get().handle(request)

        return response.toJson()
