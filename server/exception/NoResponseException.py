from server.exception.DmsException import DmsException


class NoResponseException(DmsException):

    def __init__(self):
        DmsException.__init__(self, "No Response Received")
