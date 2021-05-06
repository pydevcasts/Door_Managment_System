from server.exception.DmsException import DmsException


class UnknownException(DmsException):

    def __init__(self):
        DmsException.__init__(self, "Error!")
