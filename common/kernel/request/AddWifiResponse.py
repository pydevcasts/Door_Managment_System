from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class AddWifiResponse(Response):

    def __init__(self, accepted):
        Response.__init__(self, Request.ADD_WIFI)
        if not accepted:
            self.setError()
