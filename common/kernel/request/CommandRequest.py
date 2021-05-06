from common.kernel.request.Request import Request


class CommandRequest(Request):

    def __init__(self, code):
        Request.__init__(self, Request.COMMAND)
        self.code = code

    def addProperty(self, name, value):
        self.__dict__[name] = value
