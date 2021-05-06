from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetParamsResponse(Response):

    def __init__(self, params):
        Response.__init__(self, Request.SET_PARAMS)
        self.params = params
