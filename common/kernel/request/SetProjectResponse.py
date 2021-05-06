from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetProjectResponse(Response):

    def __init__(self, accepted):
        Response.__init__(self, Request.SET_PROJECT)
        if not accepted:
            self.setError()
