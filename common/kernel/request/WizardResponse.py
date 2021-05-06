from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class WizardResponse(Response):

    def __init__(self, state, accepted = True):
        Response.__init__(self, Request.WIZARD)
        self.state = state
        if not accepted:
            self.setError()
