from common.kernel.core.BaseDataList import BaseDataList
from common.kernel.setting.ListSetting import ListSetting

toggleList = BaseDataList({
    1: "On",
    0: "Off"
})


class ToggleSetting(ListSetting):

    ################################################################################
    def __init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault):
        ListSetting.__init__(self, settingID, title, analyzerNo, receiveIndex, factoryDefault, toggleList)
