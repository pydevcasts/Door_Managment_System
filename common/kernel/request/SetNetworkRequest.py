from common.kernel.request.Request import Request


class SetNetworkRequest(Request):

    def __init__(self, interface, dhcp, ipAddress, subnetMask, defaultGateway):
        Request.__init__(self, Request.SET_NETWORK)
        self.interface = interface
        self.dhcp = dhcp
        self.ipAddress = ipAddress
        self.subnetMask = subnetMask
        self.defaultGateway = defaultGateway
