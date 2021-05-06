from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class EnableMechanicalResponse(Response):

    def __init__(self, mechanical):
        Response.__init__(self, Request.ENABLE_MECHANICAL)
        self.mechanical = mechanical
