from common.kernel.request.Request import Request


class EnableMechanicalRequest(Request):

    def __init__(self, mechanical):
        Request.__init__(self, Request.ENABLE_MECHANICAL)
        self.mechanical = mechanical
