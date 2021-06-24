import requests
# from getmac import get_mac_address as gma
import platform
# from uuid import getnode as get_mac

from common.kernel.request.AuthenticationRequest import AuthenticationRequest
from common.kernel.request.Request import Request
from server.connection.ConnectionManager import ConnectionManager
from server.web.WebDoorListLoader import webDoorListLoader


class WebConnectionManager(ConnectionManager):
    """get url get connection type getResponseText start and stop Connection"""
    # MAC_ADDRESS = gma().upper()  # ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
    OS_NAME = platform.system() + " " + platform.release()

    ##############################################################################################
    def __init__(self, webServer, userName, password):
        ConnectionManager.__init__(self)
        self.webServer = webServer
        self.userName = userName
        self.password = password

          
        self.role = -1

        self.session = None

    ##############################################################################################
    def getConnectionType(self):
        return ConnectionManager.CONNECTION_TYPE_WEB

    ##############################################################################################
    def getURL(self, subUrl=""):
        webServer = self.webServer
        if webServer is None or len(webServer) == 0:
            return None

        if not (webServer.lower().startswith("http://") or webServer.lower().startswith("https://")):
            webServer = "http://" + webServer

        while webServer[-1:] == "/":
            webServer = webServer[:-1]

        url = webServer + "/" + subUrl
        return url

    ##############################################################################################
    def getResponseText(self, request, door):

        request = self.projectKey
        if door is not None:
            request.serial = door.serial

        setattr(request, 'clientDevice', WebConnectionManager.OS_NAME)
        setattr(request, 'clientConnection', "Web")
        setattr(request, 'clientMacAddress', WebConnectionManager.MAC_ADDRESS)
        setattr(request, 'clientUserName', self.userName)

        try:
            url = self.getURL("request/")
            if url is None:
                return None

            # headers = {'content-type': 'application/json'}
            # data = {} #get parameters
            params = {"request": request.toJson()}  # post parameters
            httpResponse = self.session.post(url, params=params, timeout=(2, 8))  # , data=data, headers=headers
            return httpResponse.text
        except Exception:
            from server.exception.CommunicationException import CommunicationException
            raise CommunicationException()

    ##############################################################################################
    def callRequest(self, request, door=None):
        response = ConnectionManager.callRequest(self, request, door)
        if response.id == Request.DOOR or response.id == Request.INFOS:
            response.__setattr__("role", self.role)
        return response

    ##############################################################################################
    def startConnection(self):
        if not self.login():
            return False

        webDoorListLoader.activate(self)
        return True

    ##############################################################################################
    def stopConnection(self):
        webDoorListLoader.deactivate()
        self.logout()

    ##############################################################################################
    def prepareDoorForDisplay(self, door):
        return True

    ##############################################################################################
    def login(self):
        self.session = requests.Session()
        try:
            response = self.callRequest(AuthenticationRequest(self.userName, self.password))
            if not response.isSuccessful():
                self.session.close()
                self.session = None
                return False
            self.projectKey = response.project
            self.role = response.role
            return True
        except:
            return False

    ##############################################################################################
    def logout(self):

        try:
            self.callRequest(AuthenticationRequest(login=False))
            self.role = -1
        except:
            pass

    ##############################################################################################
    def requestEarlyLoad(self):
        webDoorListLoader.requestEarlyLoad()

    ##############################################################################################
    def downloadLogFile(self, name):

        try:
            url = self.getURL("downloadlog")
            if url is None:
                return None

            r = self.session.get(url, allow_redirects=True)

            file = open(name, 'wb')
            file.write(r.content)
            file.close()

        except Exception:
            from server.exception.CommunicationException import CommunicationException
            raise CommunicationException()
