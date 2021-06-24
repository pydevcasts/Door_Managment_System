import threading

from Globals import ini
from common.kernel.request.Request import Request
from common.kernel.request.Response import Response
from server.core.DoorList import doorList


class ConnectionManager:
    """manage login """
    CONNECTION_TYPE_WIFI = 0
    CONNECTION_TYPE_BLUETOOTH = 1
    CONNECTION_TYPE_WEB = 2

    ##############################################################################################
    def __init__(self):
        self.lock = threading.Lock()
        self.instance = None

    ##############################################################################################
    def get(self):
        return self.instance

    ##############################################################################################
    def getConnectionType(self):
        return None

    ##############################################################################################
    def set(self, connManager):
        if self.instance is not None:
            self.instance.stopConnection()

        doorList.clear()

        if not connManager.startConnection():
            return False

        self.instance = connManager
        return True

    ##############################################################################################
    def check(self):
        if not ini.getConnectionRemember():
            return False

        if ini.getConnection() == "wifi":
            from server.wifi.WifiConnectionManager import WifiConnectionManager
            if self.set(WifiConnectionManager(ini.getProjectKey())):
                return True

        if ini.getConnection() == "web":
            from server.web.WebConnectionManager import WebConnectionManager
            if self.set(WebConnectionManager(ini.getWebServer(), ini.getWebUserName(), ini.getWebPassword())):
                return True

        return False

    ##############################################################################################
    def callRequest(self, request, door=None):

        self.lock.acquire()
        """اگر متد ()acquire با True فراخوانی شود، که آرگومان پیش فرض است 
        پس از آن تا زمانی که قفل باز نشود، اجرای رشته مسدود می شود.
        """
        try:
            responseText = self.getResponseText(request, door)
            try:
                response = Response(Request.UNDEFINED, responseText)
            except:
                # print(time.time(), self.isLive(), response.__dict__['_content'])
                # f = open('../error.html', 'wb')
                # f.write(responseText)
                # f.close()
                from server.exception.ResponseFormatException import ResponseFormatException
                raise ResponseFormatException()

            if response.isSuccessful():
                return response

            if response.error == Response.ERROR_AUTHENTICATION:
                from server.exception.AuthenticationException import AuthenticationException
                raise AuthenticationException()

            if response.error == Response.ERROR_AUTHORIZATION:
                from server.exception.AuthorizationException import AuthorizationException
                raise AuthorizationException()

            if response.getID() == request.getID():
                return response

            from server.exception.UnknownException import UnknownException
            raise UnknownException()

        finally:
            self.lock.release()
            """ این متد برای آزاد سازی قفل استفاده می شود
            . در زیر چند کار مهم مربوط به این روش آورده شده است –
            اگر lock قفل شود ، سپس متد ()release آن را باز می کند.
            وظیفه آن این است که اگر بیش از یک رشته مسدود شده و منتظر قفل شدن lock است، اجازه دهد دقیقاً یک رشته ادامه یابد."""

    ##############################################################################################
    def getResponseText(self, request, door):
        raise Exception("Unimplemented")

    ##############################################################################################
    def startConnection(self):
        raise Exception("Unimplemented")

    ##############################################################################################
    def stopConnection(self):
        raise Exception("Unimplemented")

    ##############################################################################################
    def prepareDoorForDisplay(self, door):
        raise Exception("Unimplemented")

    ##############################################################################################
    def requestEarlyLoad(self):
        pass


#################################################################################################
#################################################################################################
#################################################################################################
connectionManager = ConnectionManager()
