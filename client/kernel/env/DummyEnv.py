from client.kernel.env.AbstractEnv import AbstractEnv


class DummyEnv(AbstractEnv):
    """door status of base datalist"""
    def __init__(self):
        AbstractEnv.__init__(self)

    ############################################################################
    def createDoorStatus(self):
        from common.kernel.core.BaseDataList import BaseDataList
        from common.kernel.status.BaseStatus import BaseStatus

        dummyStatusList = BaseDataList()

        from client.kernel.status.DoorStatus import DoorStatus
        dummyStatusList.add(
            BaseStatus(0, "Dummy", "images/automatic.png", "images/automatic.gif", default=True, settingMode=True))

        return DoorStatus(dummyStatusList)
