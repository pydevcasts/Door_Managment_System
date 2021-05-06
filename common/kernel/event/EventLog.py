import time


class EventLog:
    def __init__(self, request=None, response=None):

        self.nowSeconds = int(round(time.time()))
        self.diffSeconds = 0

        try:
            self.clientDevice = request.clientDevice
        except:
            self.clientDevice = "Local"

        try:
            self.clientConnection = request.clientConnection
        except:
            self.clientConnection = "Local"

        try:
            self.clientUserName = request.clientUserName
        except:
            self.clientUserName = "Local"

        try:
            self.clientMacAddress = request.clientMacAddress
        except:
            self.clientMacAddress = "Local"

        try:
            self.door_error = response.getError()
        except:
            self.door_error = 0

        try:
            from common.kernel.core.DoorErrors import doorErrors
            from Lang import lgetDefault
            self.door_error_description = lgetDefault(doorErrors.find(self.door_error).message)
        except:
            self.door_error_description = ""

        self.title = ""
        self.description = ""
        self.param1 = ""
        self.param2 = ""
        self.param3 = ""

    def toJson(self):
        # import json
        # return json.dumps(self.__dict__)
        return self.__dict__
