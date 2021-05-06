from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetNameResponse(Response):

    def __init__(self, name, accepted):
        Response.__init__(self, Request.SET_NAME)
        self.name = name
        if not accepted:
            self.setError()
