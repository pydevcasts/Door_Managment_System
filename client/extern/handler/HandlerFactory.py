from client.extern.handler.AddWifiHandler import addWifiHandler
from client.extern.handler.BluetoothConnectionHandler import bluetoothConnectionHandler
from client.extern.handler.SetNetworkHandler import setNetworkHandler
from client.extern.handler.SetWebServerHandler import setWebServerHandler
from common.kernel.handler.HandlerFactory import HandlerFactory
from common.kernel.request.Request import Request

handlerFactory = HandlerFactory()
handlerFactory.register(Request.BLUETOOTH_CONNECTION, bluetoothConnectionHandler)
handlerFactory.register(Request.ADD_WIFI, addWifiHandler)
handlerFactory.register(Request.SET_WEB_SERVER, setWebServerHandler)
handlerFactory.register(Request.SET_NETWORK, setNetworkHandler)
