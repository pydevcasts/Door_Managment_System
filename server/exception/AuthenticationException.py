from server.exception.DmsException import DmsException


class AuthenticationException(DmsException):

    def __init__(self):
        DmsException.__init__(self, "Authentication Failed")
