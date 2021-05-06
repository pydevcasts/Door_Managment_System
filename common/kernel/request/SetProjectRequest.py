from common.kernel.request.Request import Request


class SetProjectRequest(Request):

    def __init__(self, newProject):
        Request.__init__(self, Request.SET_PROJECT)
        self.newProject = newProject
