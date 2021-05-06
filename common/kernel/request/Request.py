import json



   
class Request:
    """ Returns:
       json code and adjusment
    """
    UNDEFINED = -1
    DOOR = 1
    SET_STATUS = 2
    SET_PARAM = 3
    SET_PASSWORD = 4
    SET_NAME = 5
    SET_PROJECT = 6
    BLUETOOTH_CONNECTION = 7
    WIZARD = 8
    SSK = 9
    ADD_WIFI = 10
    INFO = 11
    COMMAND = 12
    SET_PARAMS = 13
    ENABLE_MECHANICAL = 14
    AUTHENTICATION = 15
    INFOS = 16
    ERROR = 17
    WEB_COMMUNICATION = 18
    RECENT_ERRORS = 19
    SET_WEB_SERVER = 20
    GROUP = 21
    AUTO_DETECT = 22
    SET_NETWORK = 23

    ############################################################################
    def __init__(self, id, jsonStr=None):
        self.id = id
        self.project = None
        self.serial = None
        self.password = None

        if jsonStr is not None:
            self.loadJson(jsonStr)

    ############################################################################
    def __str__(self):
        return self.__class__.__name__ + self.toJson()

    ############################################################################
    def getID(self):
        return self.id

    ############################################################################
    def toJson(self):
        return json.dumps(self.__dict__)

    ############################################################################
    def loadJson(self, jsonStr):
        try:
            dict = json.loads(jsonStr)
            self.__dict__.update(dict)
        except:
            self.id = Request.UNDEFINED
