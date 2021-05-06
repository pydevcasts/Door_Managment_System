from common.kernel.request.Request import Request


class SetParamsRequest(Request):

    def __init__(self, params):
        Request.__init__(self, Request.SET_PARAMS)
        self.params = params
