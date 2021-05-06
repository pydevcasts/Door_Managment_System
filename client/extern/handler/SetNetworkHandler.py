import subprocess
import traceback

from Globals import logger
from client.kernel.handler.HandlerA import HandlerA
from common.kernel.request.SetNetworkResponse import SetNetworkResponse


class SetNetworkHandler(HandlerA):

    ############################################################################
    def __init__(self):
        HandlerA.__init__(self)

    ############################################################################
    def getAccessRole(self, request):
        from common.kernel.core.Role import ROLE_OWNER
        return ROLE_OWNER

    ############################################################################
    def restartNetworking(self):
        logger.debug("executing: /etc/init.d/networking stop")
        subprocess.call(["/etc/init.d/networking", "stop"])
        logger.debug("executing: /etc/init.d/networking start")
        subprocess.call(["/etc/init.d/networking", "start"])

    ############################################################################
    def restartNetworkManager(self):
        # If you have some other network manager
        """
        logger.debug("executing: /etc/init.d/network-manager stop")
        subprocess.call(["/etc/init.d/network-manager", "stop"])
        logger.debug("executing: /etc/init.d/network-manager start")
        subprocess.call(["/etc/init.d/network-manager", "start"])
        """
        pass

    ############################################################################
    def tearDown(self, interface):
        logger.debug("executing: ifconfig " + interface + " down")
        subprocess.call(["ifconfig", interface, "down"])

    ############################################################################
    def bringUp(self, interface):
        logger.debug("executing: ifconfig " + interface + " up")
        subprocess.call(["ifconfig", interface, "up"])

    ############################################################################
    def enableDHCP(self, interface):

        try:
            self.restartNetworking()
            self.restartNetworkManager()

            # self.tearDown(interface)

            logger.debug("executing: ifconfig " + interface + " 0.0.0.0")
            subprocess.call(["ifconfig", interface, "0.0.0.0"])

            self.bringUp(interface)

            return SetNetworkResponse(True)

        except:
            logger.exception(traceback.format_exc())

        return SetNetworkResponse(False, "Error")

    ############################################################################
    def enableStaticIP(self, interface, ipAddress, subnetMask, defaultGateway):

        try:
            self.restartNetworking()
            self.restartNetworkManager()

            # self.tearDown(interface)

            logger.debug("executing: ifconfig " + interface + " " + ipAddress)
            subprocess.call(["ifconfig", interface, ipAddress])
            logger.debug("executing: ifconfig " + interface + " netmask " + subnetMask)
            subprocess.call(["ifconfig", interface, "netmask", subnetMask])
            logger.debug("executing: route add default gw " + defaultGateway + " " + interface)
            subprocess.call(["route", "add" "default" "gw", defaultGateway, interface])

            self.bringUp(interface)

            return SetNetworkResponse(True)

        except:
            logger.exception(traceback.format_exc())

        return SetNetworkResponse(False, "Error")

    ############################################################################
    def handle(self, request, **kwargs):

        interface = str(request.interface)

        dhcp = request.dhcp is not None and "true" == str(request.dhcp).lower()
        if dhcp:
            return self.enableDHCP(interface)

        ipAddress = str(request.ipAddress)
        subnetMask = str(request.subnetMask)
        defaultGateway = str(request.defaultGateway)
        """
        if name is None or len(name.strip()) == 0:
            return AddWifiResponse(False)

        if password is None or len(password.strip()) == 0:
            return AddWifiResponse(False)

        ssid = self.connectedNetworkSsid()
        if ssid == name:
            return AddWifiResponse(True)
        """

        return self.enableStaticIP(interface, ipAddress, subnetMask, defaultGateway)


#######################################################
#######################################################
#######################################################

setNetworkHandler = SetNetworkHandler()
