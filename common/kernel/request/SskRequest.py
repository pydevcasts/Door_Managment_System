from common.kernel.request.Request import Request


class SskRequest(Request):

    def __init__(self):
        Request.__init__(self, Request.SSK)
