from common.kernel.request.Request import Request


class SetPasswordRequest(Request):

    def __init__(self, role, oldPassword, newPassword):
        Request.__init__(self, Request.SET_PASSWORD)
        self.role = role
        self.oldPassword = oldPassword
        self.newPassword = newPassword
