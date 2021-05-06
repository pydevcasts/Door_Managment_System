from common.kernel.request.Request import Request


class BluetoothConnectionRequest(Request):

    def __init__(self):
        Request.__init__(self, Request.BLUETOOTH_CONNECTION)
