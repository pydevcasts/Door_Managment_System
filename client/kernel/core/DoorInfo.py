from Globals import ini, logger


class DoorInfo:
    """requestDoorSerial,addDoorNameListener,getName,getSerial,getProject"""
    
    
    ###########################################################################
    def __init__(self):

        self._name = ini.getDoorName()

        self._serial = None
        self.requestDoorSerial()

        self.setProject(ini.getProject())

        self.doorNameListeners = []

    ###########################################################################
    def requestDoorSerial(self):
        from client.kernel.setting.CommandImplFactory import commandImplFactory
        changeSerial = commandImplFactory.getCommandImpl(3095)  # Change Serial
        if changeSerial is None:
            return

        serialNo = changeSerial.requestDoorSerial()
        if serialNo is not None:
            self.setSerial(serialNo)

    ###########################################################################
    def addDoorNameListener(self, listener):
        if listener is not None:
            self.doorNameListeners.append(listener)

    ###########################################################################
    def getName(self):
        if self._name is None or len(self._name) < 1:
            self.setName("Deutschtec Door")
        return self._name

    ###########################################################################
    def setName(self, name, validate=True):
        if validate:
            name = self.validate(name)
            if name is None:
                return False

        self._name = name
        ini.setDoorName(self.getName())
        ini.save()

        for listener in self.doorNameListeners:
            listener.doorNameChanged(self._name)

        return True

    ###########################################################################
    def getSerial(self):
        if self._serial is None:
            self.requestDoorSerial()
        return self._serial

    ###########################################################################
    def setSerial(self, serial):
        self._serial = self.validate(serial)

    ###########################################################################
    def getProject(self):
        return self._project

    ###########################################################################
    def setProject(self, project):
        self._project = self.validate(project)
        ini.setProject(self.getProject())

    ###########################################################################
    def validate(self, text):
        if text is None:
            return None

        text = str(text).strip()
        if text == '':
            return None

        return text


###############################################################################
###############################################################################
###############################################################################
doorInfo = DoorInfo()
