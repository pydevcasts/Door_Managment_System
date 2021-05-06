from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetParamResponse(Response):

    def __init__(self, code, value):
        Response.__init__(self, Request.SET_PARAM)
        self.code = code
        self.value = value
