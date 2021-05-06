import threading
import time
import traceback

from Globals import logger
from common.kernel.request.InfosRequest import InfosRequest
from server.core.DoorList import doorList
from server.web.WebConnectionInfo import WebConnectionInfo


class WebDoorListLoader(threading.Thread):
    """ load active and run deactive and clean"""
    ###############################################################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="Web Door List Loader")
        self.setDaemon(True)

        self.webConnectionManager = None

        self.alive = True
        self.active = False
        self.counter = 0
        self.request = InfosRequest()

        from Exit import exit
        exit.register(self.cleanUp)

    ###############################################################################################################
    def load(self):
        response = self.webConnectionManager.callRequest(self.request)
        if not response.isSuccessful():
            doorList.clear()
            return

        doorList.insertInfosResponse(response, WebConnectionInfo())

    ###############################################################################################################
    def activate(self, webConnectionManager):
        self.webConnectionManager = webConnectionManager
        self.active = True

    ###############################################################################################################
    def run(self):

        maxCount = 10

        while self.alive:
            # Establish connection with client.
            try:
                if not self.active:
                    continue

                if self.counter > 0:
                    self.counter -= 1
                    continue

                self.load()
                self.counter = maxCount

            except:
                logger.exception(traceback.format_exc())
            finally:
                time.sleep(0.5)

    ##############################################################################################
    def requestEarlyLoad(self):
        if self.counter >= 2:
            self.counter = 0

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
webDoorListLoader = WebDoorListLoader()
