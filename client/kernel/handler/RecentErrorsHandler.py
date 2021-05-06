from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.RecentErrorsResponse import RecentErrorsResponse


class RecentErrorsHandler(HandlerA):

    ###############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_NONE
        return ROLE_NONE

    ###############################################################################
    def handle(self, request, **kwargs):
        from client.kernel.analyze.Analyzer1000 import analyzer1000
        response = RecentErrorsResponse(analyzer1000.getRecentErrorList())
        return response



#######################################################
#######################################################
#######################################################

recentErrorsHandler = RecentErrorsHandler()
