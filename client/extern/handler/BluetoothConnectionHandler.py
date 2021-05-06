from Globals import interface
from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.BluetoothConnectionResponse import BluetoothConnectionResponse
from common.kernel.request.DoorRequest import DoorRequest


class BluetoothConnectionHandler(HandlerA):
    """[HandlerA]:get handeling for auth and getAccessRole withcheck seriyal door"""
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
        from client.kernel.core.Authorizer import authorizer
        return authorizer.checkProjectRequest(request)

    ############################################################################
    def handle(self, request, **kwargs):

        doorRequest = DoorRequest()
        doorRequest.project = request.project # to avoid responsing to unauthorized devices
        doorRequest.password = request.password

        from client.kernel.core.DoorInfo import doorInfo
        doorRequest.serial = doorInfo.getSerial()

        response = interface.get().handle(doorRequest)
        return BluetoothConnectionResponse(response)


#######################################################
#######################################################
#######################################################

bluetoothConnectionHandler = BluetoothConnectionHandler()
