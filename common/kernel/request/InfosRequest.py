from common.kernel.request.Request import Request


class InfosRequest(Request):

    def __init__(self):
        Request.__init__(self, Request.INFOS)
