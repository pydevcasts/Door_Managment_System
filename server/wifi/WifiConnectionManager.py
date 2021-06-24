import requests
import socket
from getmac import get_mac_address as gma
"""کتابخانه مک آدرس """
import platform

from server.connection.ConnectionManager import ConnectionManager
from server.wifi.ServerUDPSender import serverUDPSender


class WifiConnectionManager(ConnectionManager):
    """system and platform"""
    MAC_ADDRESS = gma().upper()
    OS_NAME = platform.system() + " " + platform.release()
    COMPUTER_NAME = socket.gethostname()

    ##############################################################################################
    def __init__(self, projectKey):
        ConnectionManager.__init__(self)
        self.projectKey = projectKey

    ##############################################################################################
    def getConnectionType(self):
        return ConnectionManager.CONNECTION_TYPE_WIFI

    ##############################################################################################
    def getResponseText(self, request, door):

        request.project = self.projectKey
        if door is not None:
            request.password = door.password
            request.serial = door.serial

        setattr(request, 'clientDevice', WifiConnectionManager.OS_NAME)
        setattr(request, 'clientConnection', "WiFi")
        setattr(request, 'clientMacAddress', WifiConnectionManager.MAC_ADDRESS)
        setattr(request, 'clientUserName', WifiConnectionManager.COMPUTER_NAME)

        try:
            wifiConnectionInfo = door.connectionInfo
            url = "http://" + wifiConnectionInfo.ip + ":8080/deutschtec/request"
            # headers = {'content-type': 'application/json'}
            # data = {} #get parameters
            params = {"request": request.toJson()}  # post parameters
            httpResponse = requests.get(url, params=params, timeout=(2, 8))  # , data=data, headers=headers
            return httpResponse.text
        except Exception:
            from server.exception.CommunicationException import CommunicationException
            raise CommunicationException()

    ##############################################################################################
    def startConnection(self):
        serverUDPSender.activate(self.projectKey)
        return True

    ##############################################################################################
    def stopConnection(self):
        serverUDPSender.deactivate()

    ##############################################################################################
    def prepareDoorForDisplay(self, door):
        # get door password, from the user or from the cache
        from common.shell.ui.dialog.CPasswordDialog import CPasswordDialog
        passwordDialog = CPasswordDialog()
        passwordDialog.show()
        if not passwordDialog.isAccepted():
            return False
        password = passwordDialog.getPassword()
        door.password = password
        return True
