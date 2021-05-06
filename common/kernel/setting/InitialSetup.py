from Lang import INITIAL_SETUP
from common.kernel.setting.Wizard import Wizard


#####################################################################################
#####################################################################################
class InitialSetup(Wizard):

    STATE_QUESTION_1 = 1
    STATE_QUESTION_2 = 2
    STATE_SCAN_START = 3
    STATE_SCAN_PROCESS = 4
    STATE_SCAN_FINISH = 5
    STATE_SCAN_FAIL = 6
    STATE_SCAN_SUCCESS = 7

    def __init__(self):
        Wizard.__init__(self, 3020, INITIAL_SETUP, "images/initialize_setup.png")


#####################################################################################
#####################################################################################
class InitialSetup1(InitialSetup):
    def __init__(self):
        InitialSetup.__init__(self)


#####################################################################################
#####################################################################################
class InitialSetup2(InitialSetup):
    def __init__(self):
        InitialSetup.__init__(self)
