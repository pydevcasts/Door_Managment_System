from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetNetworkResponse(Response):

    def __init__(self, accepted, message=""):
        Response.__init__(self, Request.SET_NETWORK)
        if not accepted:
            self.setError()
        self.message = message
