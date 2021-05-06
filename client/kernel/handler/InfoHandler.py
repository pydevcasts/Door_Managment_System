from client.kernel.core.Authorizer import authorizer
from client.kernel.core.DoorInfo import doorInfo
from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.InfoResponse import InfoResponse


class InfoHandler(HandlerA):

    ############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ############################################################################
    def disconnectHandling(self):
        return True

    ############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_NONE
        return ROLE_NONE

    ############################################################################
    def authenticate(self, request):
        return authorizer.checkProjectRequest(request)

    ############################################################################
    def response(self, name, serial, model, version):
        return InfoResponse(name, serial, model, version)

    ############################################################################
    def handle(self, request, **kwargs):

        from client.kernel.Environment import environment
        model, version = environment.getModelVersion()
        serial = doorInfo.getSerial()

        name = doorInfo.getName()
        if name is None or str(name).strip() == "":
            import socket
            hostName = socket.gethostname()
            if hostName is not None or str(hostName).strip() != "" and "raspberry" not in hostName.lower():
                name = hostName

        if name is None or str(name).strip() == "":
            name = "Door[" + str(serial) + "]"

        response = self.response(name, serial, model, version)

        from client.kernel.serial.SerialCommunicator import serialCommunicator
        if not serialCommunicator.connected:
            response.setInvalid()
            return response

        response.setDigital()
        if serialCommunicator.mechanical:
            response.setMechanical()

        response.status = environment.getDoorStatus().getValue()

        from client.kernel.analyze.Analyzer1000 import analyzer1000
        response.doorError = analyzer1000.getSystemError()

        return response


################################################################################
################################################################################
################################################################################

infoHandler = InfoHandler()
