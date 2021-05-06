from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class RecentErrorsResponse(Response):

    def __init__(self, doorErrors):
        Response.__init__(self, Request.RECENT_ERRORS)
        self.doorErrors = doorErrors
