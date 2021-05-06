from common.kernel.core.BaseDataList import BaseData


class BaseStatus(BaseData):
    def __init__(self, key, titleKey, imageAddress, animationAddress, default=False, settingMode=False, is_open_status=False, is_locked_status=False):
        BaseData.__init__(self, key, titleKey)
        self.imageAddress = imageAddress
        self.animationAddress = animationAddress
        self.default = default
        self.settingMode = settingMode
        self.is_open_status = is_open_status
        self.is_locked_status = is_locked_status
