from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetWebServerResponse(Response):

    def __init__(self, accepted):
        Response.__init__(self, Request.SET_WEB_SERVER)
        if not accepted:
            self.setError()
