from common.kernel.request.InfoResponse import InfoResponse
from common.kernel.request.Request import Request


class DoorResponse(InfoResponse):

    def __init__(self, name, serial, model, version, role=0, **kwargs):
        InfoResponse.__init__(self, name, serial, model, version)
        self.id = Request.DOOR
        self.role = role
        self.params = {}

        self.properties = {}
        for key, value in kwargs:
            self.addProperty(key, value)

    def addProperty(self, key, value):
        if key is None:
            return
        self.properties[key] = value
