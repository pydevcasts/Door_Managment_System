from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class ErrorResponse(Response):

    def __init__(self, error):
        Response.__init__(self, Request.ERROR)
        self.setError(error)
