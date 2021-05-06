from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class CommandResponse(Response):

    def __init__(self, accepted):
        Response.__init__(self, Request.COMMAND)
        if not accepted:
            self.setError()
