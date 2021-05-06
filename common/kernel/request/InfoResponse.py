from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class InfoResponse(Response):
    CONNECTION_STATUS_INVALID = 0
    CONNECTION_STATUS_DIGITAL = 1
    CONNECTION_STATUS_MECHANICAL = 2

    def __init__(self, name, serial, model, version):
        Response.__init__(self, Request.INFO)
        self.name = name
        self.serial = serial
        self.model = model
        self.version = version
        self.connectionStatus = InfoResponse.CONNECTION_STATUS_INVALID
        self.status = 0
        self.doorError = -1

    def setInvalid(self):
        self.connectionStatus = InfoResponse.CONNECTION_STATUS_INVALID

    def setDigital(self):
        self.connectionStatus = InfoResponse.CONNECTION_STATUS_DIGITAL

    def isDigital(self):
        return self.connectionStatus == InfoResponse.CONNECTION_STATUS_DIGITAL

    def setMechanical(self):
        self.connectionStatus = InfoResponse.CONNECTION_STATUS_MECHANICAL

    def isMechanical(self):
        return self.connectionStatus == InfoResponse.CONNECTION_STATUS_MECHANICAL
