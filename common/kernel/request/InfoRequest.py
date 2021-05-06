from common.kernel.request.Request import Request


class InfoRequest(Request):

    def __init__(self):
        Request.__init__(self, Request.INFO)
