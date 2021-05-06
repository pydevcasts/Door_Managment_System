from common.kernel.request.Request import Request


class WebCommunicationRequest(Request):

    def __init__(self, project, dirty, doorResponse, recentErrorsResponse, doorEventLogs):
        Request.__init__(self, Request.WEB_COMMUNICATION)

        for k, v in recentErrorsResponse.__dict__.items():
            self.__dict__[k] = v

        for k, v in doorResponse.__dict__.items():
            self.__dict__[k] = v

        self.doorEventLogs = doorEventLogs

        self.id = Request.WEB_COMMUNICATION
        self.project = project
        self.dirty = dirty
