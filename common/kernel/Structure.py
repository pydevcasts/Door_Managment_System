from common.kernel.struct.RevolvingStruct3_00 import RevolvingStruct3_00
from common.kernel.struct.SlidingStruct1_36 import SlidingStruct1_36
from common.kernel.struct.SlidingStruct2_20 import SlidingStruct2_20


class Structure:

    #########################################################################################################
    def __init__(self):
        self.modelMap = {}

    #########################################################################################################
    def register(self, envImpl):
        model = envImpl.getModel()
        version = envImpl.getVersion()
        """getVersion, getModel is method in 
        from common.kernel.struct.RevolvingStruct3_00 import RevolvingStruct3_00
        """
        if self.modelMap.get(model, None) is None:
            self.modelMap[model] = [envImpl]
            return

        for i in range(0, len(self.modelMap[model])):
            if version < self.modelMap[model][i].getVersion():
                self.modelMap[model] = self.modelMap[model][:i] + [envImpl] + self.modelMap[model][i:]
                return

        self.modelMap[model].append(envImpl)

    #########################################################################################################
    def get(self, model, version):

        try:
            versionList = self.modelMap[model]
            size = len(versionList)
            for i in range(1, size):
                if versionList[i].getVersion() > version:
                    return versionList[i - 1]

            return versionList[-1]
        except:
            pass

        return None


################################################################################
################################################################################
################################################################################
structure = Structure()

structure.register(SlidingStruct1_36())
structure.register(SlidingStruct2_20())

structure.register(RevolvingStruct3_00())
