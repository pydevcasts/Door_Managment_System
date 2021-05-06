from common.kernel.request.Request import Request


class SetWebServerRequest(Request):

    def __init__(self, webServer):
        Request.__init__(self, Request.SET_WEB_SERVER)
        self.webServer = webServer
