import traceback

from Globals import interface, logger
from common.extern.socket.UDPCommunicator import UDPCommunicator
from common.kernel.request.Request import Request
""" قسمت سوکت پروگرامینگ هستش که استارت شده
و مداوم در حال اجرا هستش در
فواصل مشخصی گوشی من براد کست میکنه و 
درها بهش رسپانس میدن که بدونه همین الان کیا هستن اگه نبود حذف کنه تو لیست نشونش نده
"""

""" PORT_UDP_CLIENT = 20049
PORT_UDP_SERVER = 23341
summary: for UDP purposes
    Create socket and bind to address
    Establish connection with client.
"""
class ClientUDPCommunicator(UDPCommunicator):

    ###########################################################################################
    def __init__(self):
        UDPCommunicator.__init__(self, UDPCommunicator.PORT_UDP_CLIENT)

    ###############################################################################################################
    def deserialize(self, objectStr):
        return Request(Request.UNDEFINED, objectStr)

    ###########################################################################################
    def send(self, response, host):
        if host is None or host.strip() == "":
            return
        UDPCommunicator.send(response, host, UDPCommunicator.PORT_UDP_SERVER)

    ###########################################################################################
    def handle(self, request, host):

        try:
            response = interface.get().handle(request)
            self.send(response, host)
        except:
            logger.exception(traceback.format_exc())


###########################################################################################
###########################################################################################
###########################################################################################
clientUDPCommunicator = ClientUDPCommunicator()
