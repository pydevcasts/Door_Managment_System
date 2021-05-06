from common.kernel.request.Request import Request


class RecentErrorsRequest(Request):

    def __init__(self):
        Request.__init__(self, Request.RECENT_ERRORS)
