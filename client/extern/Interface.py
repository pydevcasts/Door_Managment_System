class Interface:
    """initial webServerCommunicator addDoorErrorListener addDoorNameListener
    """
    ############################################################################
    def __init__(self):
        self.kernel = None
        self.shell = None

    ############################################################################
    def start(self):

        from client.extern.socket.ClientUDPCommunicator import clientUDPCommunicator
        clientUDPCommunicator.start()
        """ قسمت سوکت پروگرامینگ هستش که استارت شده
        و مداوم در حال اجرا هستش در
        فواصل مشخصی گوشی من براد کست میکنه و 
        درها بهش رسپانس میدن که بدونه همین الان کیا هستن اگه نبود حذف کنه تو لیست نشونش نده
        """
        """
        from client.network.ClientCommunicator import clientCommunicator
        clientCommunicator.start()

        from client.network.ClientSendManager import clientSendManager
        clientSendManager.start()
        """

        from client.extern.bluetooth.BluetoothListener import bluetoothListener
        bluetoothListener.start()

        from client.extern.web.WebListener import webListener
        webListener.start()
        """ یعنی ارتباط از طریق گوشی یا لب تاب بدون وب یه 
        وب سرور کوچیکه یعنی ریکویست از طریق گوشی به در و برعکس گرفتن ریسپانس"""
        from client.extern.websocket.WebServerCommunicator import webServerCommunicator
        webServerCommunicator.start()
        """ ارتباط هر وسیله از طریق وب با در هستش 
        """
        self.kernel.addStatusListener(webServerCommunicator)
        self.kernel.addSettingListener(webServerCommunicator)
        self.kernel.addMechanicalListener(webServerCommunicator)

    ############################################################################
    def initKernel(self, kernel):
        self.kernel = kernel

    ############################################################################
    def initShell(self, shell):
        self.shell = shell

        from Lang import WEB_SERVER_URL
        from client.extern.websocket.WebServerCommunicator import webServerCommunicator
        shell.addConfiguration(WEB_SERVER_URL, webServerCommunicator.getWebServerUrl, webServerCommunicator.setWebServerUrl)

    ############################################################################
    def handle(self, request, **kwargs):
        from client.extern.handler.HandlerFactory import handlerFactory
        response = handlerFactory.handle(request, log=False, **kwargs)
        if response is None:
            response = self.kernel.handle(request, **kwargs)
        return response

    #################################################################################
    def addDoorErrorListener(self, listener):
        self.kernel.addDoorErrorListener(listener)

    #################################################################################
    def addDoorNameListener(self, listener):
        return self.kernel.addDoorNameListener(listener)
