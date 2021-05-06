from Globals import logger
from client.kernel.core.Authorizer import authorizer
from common.kernel.core.Role import ROLE_NONE
from common.kernel.request.ErrorResponse import ErrorResponse
from common.kernel.request.Response import Response


class HandlerA:
    """kernel folder"""
    """[HandlerA]:get handeling for auth and getAccessRole withcheck seriyal door"""
    ###############################################################################
    def __init__(self):
        pass

    ###############################################################################
    def disconnectHandling(self):
        return False

    ###############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_SUPERUSER
        return ROLE_SUPERUSER

    ###############################################################################
    def handle(self, request, **kwargs):
        """simple handle without security. should be implemented in subclasses"""

    ###############################################################################
    def authenticate(self, request):
        return authorizer.checkDoorRequest(request)
        """check seriyal door"""
        
    ###############################################################################
    def authorize(self, request):

        accessRole = self.getAccessRole(request)

        if accessRole == ROLE_NONE:
            return True

        if authorizer.isEmptyPassword(accessRole):
            return True

        if request is None:
            return False

        try:
            password = str(request.password)
            return authorizer.checkAccess(accessRole, password)
        except:
            pass

        return False

    ###############################################################################
    def execute(self, request, **kwargs):

        try:
            if not self.disconnectHandling():
                from client.kernel.serial.SerialCommunicator import serialCommunicator
                if not serialCommunicator.isSerialConnected():
                    return ErrorResponse(Response.ERROR_DOOR_NOT_AVAILABLE)

            security = kwargs.get('security', True)

            if security and not self.authenticate(request):
                return ErrorResponse(Response.ERROR_AUTHENTICATION)

            if security and not self.authorize(request):
                return ErrorResponse(Response.ERROR_AUTHORIZATION)

            return self.handle(request, **kwargs)

        except:
            import traceback
            logger.exception(traceback.format_exc())

        return ErrorResponse(Response.ERROR_UNKNOWN)

    def createEventLog(self, request, response):
        return None
