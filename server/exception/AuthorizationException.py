from server.exception.DmsException import DmsException


class AuthorizationException(DmsException):

    def __init__(self):
        DmsException.__init__(self, "Authorization Failed")
