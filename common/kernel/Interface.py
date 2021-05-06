from Globals import logger
from Lang import lget, WELCOME, VERSION
from Version import client_version


class Interface:

    ######################################################################################
    def __init__(self):
        self.initialCheck()
        self.initJsonEncoder()

    ######################################################################################
    def initialCheck(self):
        try:
            from pyDes import des
            """This algorithm is a pure python implementation of the DES and Triple DES algorithms. 
            Triple DES is either DES-EDE3 with a 24 byte key, or DES-EDE2 with a 16 byte key
            یک پیاده سازی پایتون خالص از الگوریتم های رمزنگاری DES و TRIPLE DES."""
        except:
            print("'PyDes' is not installed. Execute: 'sudo pip install PyDes'")
            import sys
            sys.exit()

    ######################################################################################
    def initJsonEncoder(self):
        from json import JSONEncoder

        def _default(self_, obj):
            return getattr(obj.__class__, "toJson", _default.default)(obj)

        _default.default = JSONEncoder().default
        JSONEncoder.default = _default

    ######################################################################################
    def start(self):
        # First Log, welcome message
        version = lget(VERSION) + " " + client_version
        logger.info(lget(WELCOME, version))
