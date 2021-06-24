from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class BluetoothConnectionResponse(Response):

    def __init__(self, doorResponse):
        Response.__init__(self, Request.BLUETOOTH_CONNECTION)
        self.__dict__ = doorResponse.__dict__.copy()
        self.id = Request.BLUETOOTH_CONNECTION

        """blutooth request sent and get response with json or dict python
        """