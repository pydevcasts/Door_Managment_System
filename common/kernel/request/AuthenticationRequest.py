from common.kernel.request.Request import Request


class AuthenticationRequest(Request):

    def __init__(self, userName = "", password = "", login = True):
        Request.__init__(self, Request.AUTHENTICATION)
        self.userName = userName
        self.password = password
        self.login = login
