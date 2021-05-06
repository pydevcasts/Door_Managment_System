from common.kernel.request.Request import Request


class AddWifiRequest(Request):

    def __init__(self, name, newPassword):
        Request.__init__(self, Request.ADD_WIFI)
        self.name = name
        self.newPassword = newPassword
