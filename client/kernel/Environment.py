from client.kernel.env.DummyEnv import DummyEnv
from client.kernel.env.RevolvingEnv3_00 import RevolvingEnv3_00
from client.kernel.env.SlidingEnv1_36 import SlidingEnv1_36
from client.kernel.env.SlidingEnv2_20 import SlidingEnv2_20
from common.kernel.Structure import Structure


class Environment(Structure):
    """درهای revolving and اسلایدی و میکروسکوپی

    Args:
        Structure ([type]): [تو محیط چه دری داری کار میکنی]

    Returns:
        [type]: [getDoorStatus, version and model,updateVersion,notifyVersionFound,versionListeners]
    """
    #########################################################################################################
    def __init__(self):
        Structure.__init__(self)

        self.dummy = DummyEnv()

        self.model = None
        self.version = None

        self.versionListeners = []

    #########################################################################################################
    def updateVersion(self, dataList):
        if self.isVersionValid():
            return

        model = "".join([chr(dataList[i]) for i in range(12, 17)])
        self.model = self.validateModel(model)
        self.version = "".join([chr(dataList[i]) for i in range(17, 24)])[1:-2]
        self.notifyVersionFound()

    #########################################################################################################
    def validateModel(self, model):
        from common.kernel.struct.AbstractStruct import MasterModel
        if model in MasterModel.models:
            return model
        return MasterModel.SLIDING

    #########################################################################################################
    def isVersionValid(self):
        return self.version is not None

    #########################################################################################################
    def getModel(self):
        return self.model

    #########################################################################################################
    def getVersion(self):
        return self.version

    #########################################################################################################
    def getModelVersion(self):
        return self.getModel(), self.getVersion()

    #########################################################################################################
    def addVersionListener(self, versionListener):
        if versionListener is None:
            return

        self.versionListeners.append(versionListener)
        if self.isVersionValid():  # version found before
            versionListener.versionFound(self.getModel(), self.getVersion())
        
    #########################################################################################################
    def notifyVersionFound(self):
        for versionListener in self.versionListeners:
            versionListener.versionFound(self.getModel(), self.getVersion())

    #########################################################################################################
    def get(self):

        model, version = self.getModelVersion()
        result = Structure.get(self, model, version)
        if result is not None:
            return result
        return self.dummy

    #########################################################################################################
    def getDoorStatus(self):
        return self.get().getDoorStatus()

    #########################################################################################################
    def getSettings(self):
        return self.get().getSettings()


################################################################################
################################################################################
################################################################################
environment = Environment()

environment.register(SlidingEnv1_36())
environment.register(SlidingEnv2_20())

environment.register(RevolvingEnv3_00())
