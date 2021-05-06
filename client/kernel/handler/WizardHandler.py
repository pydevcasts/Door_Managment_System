import time

from Globals import logger
from client.kernel.handler.HandlerA import HandlerA
from client.kernel.setting.CommandImplFactory import commandImplFactory
from common.kernel.request.WizardResponse import WizardResponse
from common.kernel.setting.Wizard import Wizard


###########################################################################
###########################################################################
class WizardHandler(HandlerA):

    #######################################################################
    def __init__(self):
        HandlerA.__init__(self)

    #######################################################################
    def getAccessRole(self, request):
        from client.kernel.Environment import environment
        simple, advanced = environment.getSettings()

        from common.kernel.core.Role import ROLE_OWNER, ROLE_INSTALLER

        if simple.find(request.code) is not None:
            return ROLE_OWNER

        return ROLE_INSTALLER

    #######################################################################
    def handle(self, request, **kwargs):
        state = Wizard.STATE_FAIL
        try:
            wizardImpl = commandImplFactory.getCommandImpl(request.code)
            newState = request.state
            if newState == Wizard.STATE_IGNORE:
                accepted = True
            elif newState == Wizard.STATE_START:
                accepted = wizardImpl.start()
            elif newState == Wizard.STATE_CANCEL:
                accepted = wizardImpl.cancel()
            else:
                accepted = wizardImpl.setState(newState)

            if newState != Wizard.STATE_IGNORE:
                time.sleep(0.5)

            state = wizardImpl.getBufferedState()
        except:
            import traceback
            logger.exception(traceback.format_exc())
            accepted = False

        return WizardResponse(state, accepted)


###########################################################################
###########################################################################
###########################################################################
wizardHandler = WizardHandler()
