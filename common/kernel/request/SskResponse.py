from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SskResponse(Response):

    def __init__(self, accepted):
        Response.__init__(self, Request.SSK)
        if not accepted:
            self.setError()
