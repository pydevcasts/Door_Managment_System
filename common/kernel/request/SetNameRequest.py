from common.kernel.request.Request import Request


class SetNameRequest(Request):

    def __init__(self, name):
        Request.__init__(self, Request.SET_NAME)
        self.name = name
