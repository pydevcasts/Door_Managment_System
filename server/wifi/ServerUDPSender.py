import threading
import time
import traceback

from Globals import logger
from common.extern.socket.UDPCommunicator import UDPCommunicator
from server.core.DoorList import doorList


class ServerUDPSender(threading.Thread):

    ###############################################################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="UDP Broadcasting on port " + str(UDPCommunicator.PORT_UDP_CLIENT))
        self.setDaemon(True)

        self.alive = True
        self.active = False
        self.broadcastRequest = None

        from Exit import exit
        exit.register(self.cleanUp)
        """exit from app"""

    ###############################################################################################################
    def broadcast(self):
        UDPCommunicator.send(self.broadcastRequest, '255.255.255.255', UDPCommunicator.PORT_UDP_CLIENT)

    ###############################################################################################################
    def activate(self, projectKey):
        from common.kernel.request.InfoRequest import InfoRequest
        self.broadcastRequest = InfoRequest()
        self.broadcastRequest.project = projectKey
        """the project is a method in request class
        """
        self.active = True

    ###############################################################################################################
    def run(self):

        while self.alive:
            # Establish connection with client.
            try:
                if not self.active:
                    time.sleep(0.5)
                    continue

                self.broadcast()
                doorList.progress()
                """lock and release door"""
                time.sleep(3)

            except:
                logger.exception(traceback.format_exc())

    ###############################################################################################################
    def deactivate(self):
        self.active = False

    ###############################################################################################################
    def cleanUp(self):
        self.deactivate()
        self.alive = False


###########################################################################################
###########################################################################################
###########################################################################################
serverUDPSender = ServerUDPSender()
