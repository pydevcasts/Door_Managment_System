from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class WebCommunicationResponse(Response):

    def __init__(self, dict):
        Response.__init__(self, Request.WEB_COMMUNICATION)

        for k, v in dict.items():
            self.__dict__[k] = v

        self.id = Request.WEB_COMMUNICATION
        str(self.live)
        str(self.requests)
