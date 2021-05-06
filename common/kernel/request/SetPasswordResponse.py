from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetPasswordResponse(Response):

    def __init__(self, role, accepted):
        Response.__init__(self, Request.SET_PASSWORD)
        self.role = role
        if not accepted:
            self.setError()
