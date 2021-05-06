from common.kernel.request.Request import Request


class DoorRequest(Request):

    def __init__(self):
        Request.__init__(self, Request.DOOR)
