from Lang import FACTORY_RESET
from common.kernel.setting.Command import Command


#####################################################################################
#####################################################################################
class FactoryReset(Command):
    def __init__(self):
        Command.__init__(self, 3021, FACTORY_RESET, "images/factory_reset.png")


#####################################################################################
#####################################################################################
class FactoryReset1(FactoryReset):
    def __init__(self):
        FactoryReset.__init__(self)


#####################################################################################
#####################################################################################
class FactoryReset2(FactoryReset):
    def __init__(self):
        FactoryReset.__init__(self)
        """supper.__init__(self)
        """
