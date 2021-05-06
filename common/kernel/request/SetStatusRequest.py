from common.kernel.request.Request import Request


class SetStatusRequest(Request):

    def __init__(self, status):
        Request.__init__(self, Request.SET_STATUS)
        """یه پیغامی از گوشی یا وب یا بلوتوث برای ما ارسال میشه
        """
        self.status = status
