from Lang import MANUAL, SUMMER_AUTOMATIC, AUTOMATIC, CONSTANT, LOCK
from common.kernel.core.BaseDataList import BaseDataList
from common.kernel.status.BaseStatus import BaseStatus


revolvingStatusList = BaseDataList()
revolvingStatusList.add(BaseStatus(1, MANUAL, "images/manual.png", None, settingMode=True))
revolvingStatusList.add(BaseStatus(2, SUMMER_AUTOMATIC, "images/summer_automatic.png", None, default=True))
revolvingStatusList.add(BaseStatus(3, AUTOMATIC, "images/automatic_r.png", None))
revolvingStatusList.add(BaseStatus(5, CONSTANT, "images/constant.png", None))
revolvingStatusList.add(BaseStatus(4, LOCK, "images/lock_r.png", None, is_locked_status=True))
