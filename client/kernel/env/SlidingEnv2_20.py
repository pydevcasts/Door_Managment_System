from client.kernel.env.SlidingEnv1_36 import SlidingEnv1_36
from common.kernel.struct.SlidingStruct2_20 import SlidingStruct2_20


class SlidingEnv2_20(SlidingStruct2_20, SlidingEnv1_36):
    """createAnalyzers of Analyzer1500,Analyzer1501,Analyzer1502,Analyzer1504"""
    ###################################################################################################################################
    def __init__(self):
        SlidingStruct2_20.__init__(self)
        SlidingEnv1_36.__init__(self)

    ###################################################################################################################################
    def createAnalyzers(self):
        from client.kernel.analyze.Analyzer1500 import Analyzer1500
        from client.kernel.analyze.Analyzer1501 import Analyzer1501
        from client.kernel.analyze.Analyzer1502 import Analyzer1502
        from client.kernel.analyze.Analyzer1504 import Analyzer1504

        return [Analyzer1500(), Analyzer1501(), Analyzer1502(), Analyzer1504()]
