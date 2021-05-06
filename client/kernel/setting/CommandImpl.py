
class CommandImpl:

    ################################################################################
    def __init__(self):
        from client.kernel.setting.CommandImplFactory import commandImplFactory
        commandImplFactory.register(self)

    ###############################################################################
    def __repr__(self):
        return self.__class__.__name__ + "[" + str(self.getParameterCode()) + "]"

    ################################################################################
    def getParameterCode(self):
        raise Exception("getParameterCode - Not Implemented")

    ################################################################################
    def getModelVersion(self):
        from common.kernel.struct.AbstractStruct import MasterModel
        return MasterModel.DUMMY, "0.00"

    ################################################################################
    def execute(self, request):
        raise Exception("execute - Not Implemented")
