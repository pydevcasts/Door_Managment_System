import subprocess
import time
import traceback

from Globals import logger
from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.AddWifiResponse import AddWifiResponse


class AddWifiHandler(HandlerA):
    """[HandlerA]:get handeling for auth and getAccessRole withcheck seriyal door"""
    """connect network and remove it add select wifi ...."""

    ############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_OWNER
        return ROLE_OWNER

    ############################################################################
    def handle(self, request, **kwargs):

        name = str(request.name)
        password = str(request.newPassword)

        if name is None or len(name.strip()) == 0:
            return AddWifiResponse(False)

        if password is None or len(password.strip()) == 0:
            return AddWifiResponse(False)

        ssid = self.connectedNetworkSsid()
        if ssid == name:
            return AddWifiResponse(True)

        connectedIndex = self.connectedNetworkIndex()

        index = self.addNetwork()
        if index < 0:
            return AddWifiResponse(False)

        self.setNetwork(index, name, password)

        connected = self.selectNetwork(index)
        if not connected:
            self.removeNetwork(index)
            if connectedIndex >= 0:
                self.selectNetwork(connectedIndex)
            return AddWifiResponse(False)

        self.saveNetwork()

        return AddWifiResponse(True)

    ############################################################################
    def addNetwork(self):
        try:
            logger.debug("executing: wpa_cli -i wlan0 add_network")
            output = subprocess.check_output(["wpa_cli", "-i", "wlan0", "add_network"])
            logger.debug("output:\n" + output)
            outputLine = self.stringLine(output, 0)
            return int(outputLine)
        except:
            logger.exception(traceback.format_exc())
            return -1

    ############################################################################
    def setNetwork(self, index, name, password):
        self.setNetworkProperty(index, "ssid", name)
        self.setNetworkProperty(index, "psk", password)

    ############################################################################
    def setNetworkProperty(self, index, name, value):
        try:
            logger.debug("executing: wpa_cli -i wlan0 set_network " + str(index) + " " + name + ' "' + value + '"')
            subprocess.call(["wpa_cli", "-i", "wlan0", "set_network", str(index), name, '"' + value + '"'])
        except:
            logger.exception(traceback.format_exc())

    ############################################################################
    def selectNetwork(self, index):
        try:
            logger.debug("executing: wpa_cli -i wlan0 select_network " + str(index))
            subprocess.call(["wpa_cli", "-i", "wlan0", "select_network", str(index)])

            for i in range(0, 5):
                time.sleep(1)
                state = self.getState()
                if state == "COMPLETED":
                    return self.connectedNetworkIndex() >= 0

            return False

        except:
            logger.exception(traceback.format_exc())
            return False

    ############################################################################
    def getCompleteStatus(self):
        try:
            logger.debug("executing: wpa_cli -i wlan0 status")
            output = subprocess.check_output(["wpa_cli", "-i", "wlan0", "status"])
            logger.debug("output:\n" + output)
            return output
        except:
            logger.exception(traceback.format_exc())
            return None

    ############################################################################
    def getState(self, completeStatus = None):
        if completeStatus is None:
            completeStatus = self.getCompleteStatus()
        return self.stringFind(completeStatus, 'wpa_state')

    ############################################################################
    def connectedNetworkSsid(self):
        try:
            completeStatus = subprocess.check_output(["wpa_cli", "-i", "wlan0", "status"])
            state = self.getState(completeStatus)
            if state != 'COMPLETED':
                return -1
            return self.stringFind(completeStatus, 'ssid')
        except:
            logger.exception(traceback.format_exc())
            return -1

    ############################################################################
    def connectedNetworkIndex(self):
        try:
            completeStatus = subprocess.check_output(["wpa_cli", "-i", "wlan0", "status"])
            state = self.getState(completeStatus)
            if state != 'COMPLETED':
                return -1
            index = int(self.stringFind(completeStatus, 'id'))
            return int(index)
        except:
            logger.debug(traceback.format_exc())
            return -1

    ############################################################################
    def removeNetwork(self, index):
        try:
            logger.debug("executing: wpa_cli -i wlan0 remove_network " + str(index))
            subprocess.call(["wpa_cli", "-i", "wlan0", "remove_network", str(index)])
        except:
            logger.exception(traceback.format_exc())

    ############################################################################
    def saveNetwork(self):
        try:
            logger.debug("executing: wpa_cli -i wlan0 save_config")
            subprocess.call(["wpa_cli", "-i", "wlan0", "save_config"])
        except:
            logger.exception(traceback.format_exc())

    ############################################################################
    def stringLine(self, text, index):
        try:
            strList = text.split('\n')
            return strList[index].strip()
        except:
            logger.exception(traceback.format_exc())
            return None

    ############################################################################
    def stringFind(self, text, key):
        try:
            lines = text.split('\n')
            for line in lines:
                if line.strip().startswith(key + "="):
                    valueStart = len(key) + 1
                    value = line.strip()[valueStart:]
                    return value.strip()
        except:
            logger.exception(traceback.format_exc())

        return None


#######################################################
#######################################################
#######################################################

addWifiHandler = AddWifiHandler()
