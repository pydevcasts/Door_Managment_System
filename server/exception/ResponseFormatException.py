from server.exception.DmsException import DmsException


class ResponseFormatException(DmsException):

    def __init__(self):
        DmsException.__init__(self, "Invalid Response Format")
