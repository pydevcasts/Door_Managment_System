from client.kernel.core.Authorizer import authorizer
from client.kernel.handler.InfoHandler import InfoHandler
from common.kernel.request.DoorResponse import DoorResponse


class DoorHandler(InfoHandler):
    """ getAccessRole,authenticate, response"""
    ############################################################################
    def __init__(self):
        InfoHandler.__init__(self)

    ############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_USER
        return ROLE_USER

    ############################################################################
    def authenticate(self, request):
        return authorizer.checkDoorRequest(request)

    ############################################################################
    def response(self, name, serial, model, version):
        return DoorResponse(name, serial, model, version)

    ############################################################################
    def handle(self, request, **kwargs):

        response = InfoHandler.handle(self, request)

        password = str(request.password)

        response.role = authorizer.getRole(password)

        if not response.isDigital():
            return response

        params = {}

        security = kwargs.get('security', True)

        from client.kernel.setting.SettingsManager import settingsManager

        # Send settings values to owners
        from common.kernel.core.Role import ROLE_OWNER
        if not security or authorizer.checkAccess(ROLE_OWNER, password):
            for setting in settingsManager.simpleSettingList:
                if setting.getValue() is not None:
                    params[str(setting.getParameterCode())] = setting.getValue()

        # Send advanced settings values to installers
        from common.kernel.core.Role import ROLE_INSTALLER
        if not security or authorizer.checkAccess(ROLE_INSTALLER, password):
            for setting in settingsManager.advancedSettingList:
                if setting.getValue() is not None:
                    params[str(setting.getParameterCode())] = setting.getValue()

        response.params = params

        from client.kernel.analyze.Analyzer1000 import analyzer1000
        response.addProperty("position", analyzer1000.position)

        return response


################################################################################
################################################################################
################################################################################

doorHandler = DoorHandler()
