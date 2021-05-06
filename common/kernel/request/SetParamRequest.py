from common.kernel.request.Request import Request


class SetParamRequest(Request):

    def __init__(self, code, value):
        Request.__init__(self, Request.SET_PARAM)
        self.code = code
        self.value = value
