from Lang import lget


class DmsException(Exception):

    ############################################################################
    def __init__(self, message):  # ,*args,**kwargs
        Exception.__init__(self)
        self.message = message

    ############################################################################
    def __repr__(self):
        return lget(str(self.message))

    ############################################################################
    def __str__(self):
        return lget(str(self.message))
