from common.extern.socket.UDPCommunicator import UDPCommunicator
from common.kernel.request.Request import Request
from common.kernel.request.Response import Response
from server.wifi.WifiConnectionInfo import WifiConnectionInfo


class ServerUDPReceiver(UDPCommunicator):

    ###########################################################################################
    def __init__(self):
        UDPCommunicator.__init__(self, UDPCommunicator.PORT_UDP_SERVER)

    ###############################################################################################################
    def deserialize(self, objectStr):
        return Response(Request.UNDEFINED, objectStr)

    ###########################################################################################
    def handle(self, response, host):
        if response is None or not response.isSuccessful():
            return

        from server.core.DoorList import doorList
        doorList.insert(response, WifiConnectionInfo(host, response.serial))


###########################################################################################
###########################################################################################
###########################################################################################
serverUDPReceiver = ServerUDPReceiver()
