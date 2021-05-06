from server.exception.DmsException import DmsException


class CommunicationException(DmsException):

    def __init__(self):
        DmsException.__init__(self, "Communication Problem")
