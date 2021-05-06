from Lang import *

ERROR_TYPE_UNKNOWN = -1
ERROR_TYPE_OK = 0
ERROR_TYPE_INFO = 1
ERROR_TYPE_COMMON = 2
ERROR_TYPE_CRITICAL = 3
ERROR_TYPE_ABSOLUTE = 4


#################################################################################
#################################################################################
class DoorError:
    def __init__(self, errorType, code, message):
        self.errorType = errorType
        self.code = code
        self.message = message

    def __repr__(self):
        return lget(self.message)

    def __str__(self):
        return self.__repr__()


#################################################################################
#################################################################################
class DoorErrors:

    #############################################################################
    def __init__(self):
        self.errors = []

        self.add(ERROR_TYPE_OK, 0, DOOR_ERROR_0)
        self.add(ERROR_TYPE_INFO, 10, DOOR_ERROR_10)
        self.add(ERROR_TYPE_INFO, 11, DOOR_ERROR_11)
        self.add(ERROR_TYPE_INFO, 12, DOOR_ERROR_12)
        self.add(ERROR_TYPE_INFO, 13, DOOR_ERROR_13)
        self.add(ERROR_TYPE_INFO, 14, DOOR_ERROR_14)
        self.add(ERROR_TYPE_INFO, 15, DOOR_ERROR_15)
        self.add(ERROR_TYPE_INFO, 16, DOOR_ERROR_16)
        self.add(ERROR_TYPE_INFO, 17, DOOR_ERROR_17)
        self.add(ERROR_TYPE_COMMON, 100, DOOR_ERROR_100)
        self.add(ERROR_TYPE_COMMON, 101, DOOR_ERROR_101)
        self.add(ERROR_TYPE_COMMON, 109, DOOR_ERROR_109)
        self.add(ERROR_TYPE_COMMON, 110, DOOR_ERROR_110)
        self.add(ERROR_TYPE_COMMON, 111, DOOR_ERROR_111)
        self.add(ERROR_TYPE_COMMON, 112, DOOR_ERROR_112)
        self.add(ERROR_TYPE_COMMON, 120, DOOR_ERROR_120)
        self.add(ERROR_TYPE_COMMON, 121, DOOR_ERROR_121)
        self.add(ERROR_TYPE_COMMON, 130, DOOR_ERROR_130)
        self.add(ERROR_TYPE_COMMON, 141, DOOR_ERROR_141)
        self.add(ERROR_TYPE_COMMON, 142, DOOR_ERROR_142)
        self.add(ERROR_TYPE_COMMON, 144, DOOR_ERROR_144)
        self.add(ERROR_TYPE_COMMON, 145, DOOR_ERROR_145)
        self.add(ERROR_TYPE_COMMON, 200, DOOR_ERROR_200)
        self.add(ERROR_TYPE_COMMON, 201, DOOR_ERROR_201)
        self.add(ERROR_TYPE_COMMON, 202, DOOR_ERROR_202)
        self.add(ERROR_TYPE_CRITICAL, 210, DOOR_ERROR_210)
        self.add(ERROR_TYPE_CRITICAL, 211, DOOR_ERROR_211)
        self.add(ERROR_TYPE_CRITICAL, 215, DOOR_ERROR_215)
        self.add(ERROR_TYPE_CRITICAL, 220, DOOR_ERROR_220)
        self.add(ERROR_TYPE_CRITICAL, 222, DOOR_ERROR_222)
        self.add(ERROR_TYPE_CRITICAL, 223, DOOR_ERROR_223)
        self.add(ERROR_TYPE_CRITICAL, 224, DOOR_ERROR_224)
        self.add(ERROR_TYPE_CRITICAL, 230, DOOR_ERROR_230)
        self.add(ERROR_TYPE_CRITICAL, 231, DOOR_ERROR_231)
        self.add(ERROR_TYPE_CRITICAL, 232, DOOR_ERROR_232)
        self.add(ERROR_TYPE_CRITICAL, 233, DOOR_ERROR_233)
        self.add(ERROR_TYPE_CRITICAL, 236, DOOR_ERROR_236)
        self.add(ERROR_TYPE_CRITICAL, 237, DOOR_ERROR_237)
        self.add(ERROR_TYPE_CRITICAL, 238, DOOR_ERROR_238)
        self.add(ERROR_TYPE_CRITICAL, 239, DOOR_ERROR_239)
        self.add(ERROR_TYPE_ABSOLUTE, 240, DOOR_ERROR_240)
        self.add(ERROR_TYPE_ABSOLUTE, 241, DOOR_ERROR_241)
        self.add(ERROR_TYPE_ABSOLUTE, 242, DOOR_ERROR_242)
        self.add(ERROR_TYPE_ABSOLUTE, 243, DOOR_ERROR_243)
        self.add(ERROR_TYPE_ABSOLUTE, 244, DOOR_ERROR_244)
        self.add(ERROR_TYPE_ABSOLUTE, 245, DOOR_ERROR_245)
        self.add(ERROR_TYPE_ABSOLUTE, 250, DOOR_ERROR_250)
        self.add(ERROR_TYPE_ABSOLUTE, 251, DOOR_ERROR_251)
        self.add(ERROR_TYPE_ABSOLUTE, 252, DOOR_ERROR_252)
        self.add(ERROR_TYPE_ABSOLUTE, 253, DOOR_ERROR_253)
        self.add(ERROR_TYPE_ABSOLUTE, 254, DOOR_ERROR_254)

    #############################################################################
    def add(self, errorType, code, message):
        self.errors.append(DoorError(errorType, code, message))

    #############################################################################
    def find(self, code):
        for error in self.errors:
            if error.code == code:
                return error

        return None

    #############################################################################
    def getImageAddress(self, code):
        error = self.find(code)
        if error is None:
            return "images/error_unknown.png"

        if error.errorType == ERROR_TYPE_OK:
            return "images/error_ok.png"
        if error.errorType == ERROR_TYPE_INFO:
            return "images/error_info.png"
        if error.errorType == ERROR_TYPE_COMMON:
            return "images/error_common.png"
        if error.errorType == ERROR_TYPE_CRITICAL:
            return "images/error_critical.png"
        if error.errorType == ERROR_TYPE_ABSOLUTE:
            return "images/error_absolute.png"

        return "images/error_unknown.png"


#################################################################################
#################################################################################
#################################################################################
doorErrors = DoorErrors()
