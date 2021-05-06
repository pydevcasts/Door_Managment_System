from client.kernel.env.AbstractEnv import AbstractEnv
from common.kernel.struct.SlidingStruct1_36 import SlidingStruct1_36


class SlidingEnv1_36(SlidingStruct1_36, AbstractEnv):
    """createAnalyzers of Analyzer1500"""
    ###################################################################################################################################
    def __init__(self):
        SlidingStruct1_36.__init__(self)
        AbstractEnv.__init__(self)

    ###################################################################################################################################
    def createAnalyzers(self):
        from client.kernel.analyze.Analyzer1500 import Analyzer1500
        return [Analyzer1500()]
