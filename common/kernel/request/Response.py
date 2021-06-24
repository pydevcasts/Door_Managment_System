import json


class Response:
    ERROR_SUCCESS = 0
    ERROR_UNKNOWN = 1
    ERROR_DOOR_NOT_AVAILABLE = 2
    ERROR_AUTHENTICATION = 3
    ERROR_AUTHORIZATION = 4

    ############################################################################
    def __init__(self, id, jsonStr=None):
        self.id = id
        self.error = Response.ERROR_SUCCESS
        self.buffered = False

        if jsonStr is not None:
            self.loadJson(jsonStr)

    ############################################################################
    def __str__(self):
        return self.__class__.__name__ + self.toJson()

    ############################################################################
    def toJson(self):
        return json.dumps(self.__dict__)

    ############################################################################
    def loadJson(self, jsonStr):
        dict = json.loads(jsonStr)
        self.__dict__.update(dict)

    ############################################################################
    def getID(self):
        return self.id

    ############################################################################
    def getError(self):
        return self.error

    ############################################################################
    def setError(self, error=ERROR_UNKNOWN):
        self.error = error

    ############################################################################
    def isSuccessful(self):
        return self.error == Response.ERROR_SUCCESS
        """error is false
        """

    ############################################################################
    def isBuffered(self):
        return "true" == str(self.buffered).lower()
        """return "true"
        """
