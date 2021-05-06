from common.kernel.request.Request import Request
from common.kernel.setting.Wizard import Wizard


class WizardRequest(Request):

    def __init__(self, code, state = Wizard.STATE_IGNORE):
        Request.__init__(self, Request.WIZARD)
        self.code = code
        self.state = state

    def ignore(self):
        self.state = Wizard.STATE_IGNORE

    def start(self):
        self.state = Wizard.STATE_START

    def cancel(self):
        self.state = Wizard.STATE_CANCEL
