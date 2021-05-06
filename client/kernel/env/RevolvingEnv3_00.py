from client.kernel.env.AbstractEnv import AbstractEnv
from common.kernel.struct.RevolvingStruct3_00 import RevolvingStruct3_00


class RevolvingEnv3_00(RevolvingStruct3_00, AbstractEnv):
    """createAnalyzers of Analyzer1500"""
    ###################################################################################################################################
    def __init__(self):
        RevolvingStruct3_00.__init__(self)
        AbstractEnv.__init__(self)

    ###################################################################################################################################
    def createAnalyzers(self):
        from client.kernel.analyze.Analyzer1500 import Analyzer1500
        return [Analyzer1500()]
