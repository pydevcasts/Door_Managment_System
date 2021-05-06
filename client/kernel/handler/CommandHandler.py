from Globals import logger, SIMULATION_ENABLED
from client.kernel.handler.HandlerA import HandlerA
from client.kernel.setting.CommandImplFactory import commandImplFactory
from common.kernel.request.CommandResponse import CommandResponse


###########################################################################
###########################################################################
class CommandHandler(HandlerA):
    """getAccessRole,createEventLog,DummyCommandHandler """
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
        accepted = False
        try:
            accepted = commandImplFactory.execute(request)
        except:
            import traceback
            logger.exception(traceback.format_exc())
            accepted = False

        return CommandResponse(accepted)

    ###############################################################################
    def createEventLog(self, request, response):
        eventLog = None
        try:
            from client.kernel.setting.SettingsManager import settingsManager
            commandImpl = commandImplFactory.getCommandImpl(request.code)

            from client.kernel.event.EventLog import EventLog
            eventLog = EventLog(request, response)

            eventLog.title = commandImpl.getTitle() + ' executed'
            eventLog.description = commandImpl.getTitle() + ' has been executed.'
            eventLog.param1 = request.code
        except:
            pass

        return eventLog


###########################################################################
###########################################################################
class DummyCommandHandler(CommandHandler):

    #######################################################################
    def __init__(self):
        CommandHandler.__init__(self)

    #######################################################################
    def handle(self, request):
        import time
        time.sleep(2)
        return CommandResponse(True)


###########################################################################
###########################################################################
###########################################################################

commandHandler = None
if SIMULATION_ENABLED:
    commandHandler = DummyCommandHandler()
else:
    commandHandler = CommandHandler()
