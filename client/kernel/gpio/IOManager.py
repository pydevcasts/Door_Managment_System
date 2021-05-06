from client.kernel.gpio.IOTask import IOTask


class IOManager:

    LeftLedPin = 5
    RightLedPin = 6

    LeftButtonPin = 16
    RightButtonPin = 13

    def __init__(self):
        pass

    def start(self):
        IOTask(buttonPin=IOManager.LeftButtonPin, ledPin=IOManager.LeftLedPin, task=self.systemReset, seconds=10).start()

    def systemReset(self):

        from client.kernel.core.DoorInfo import doorInfo
        doorInfo.setProject("")
        doorInfo.setName("", False)

        from client.kernel.core.Authorizer import authorizer
        authorizer.resetPasswords()


####################################################################################
####################################################################################
####################################################################################
ioManager = IOManager()