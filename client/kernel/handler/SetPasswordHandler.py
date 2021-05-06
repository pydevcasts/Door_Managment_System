from client.kernel.core.Authorizer import authorizer
from client.kernel.handler.HandlerA import HandlerA
from common.kernel.core.Role import ROLE_SUPERUSER
from common.kernel.request.SetPasswordResponse import SetPasswordResponse


class SetPasswordHandler(HandlerA):

    ###############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ###############################################################################
    def getAccessRole(self, request):
        try:
            return int(request.role)
        except:
            pass

        return ROLE_SUPERUSER

    ###############################################################################
    def handle(self, request, **kwargs):
        role = request.role
        oldPassword = request.oldPassword
        newPassword = request.newPassword

        if not authorizer.checkPassword(role, oldPassword):
            return SetPasswordResponse(role, False)

        if newPassword is None or len(newPassword) == 0:
            return SetPasswordResponse(role, False)

        authorizer.setPassword(role, newPassword)
        return SetPasswordResponse(role, True)


#######################################################
#######################################################
#######################################################

setPasswordHandler = SetPasswordHandler()
