from Lang import AUTOMATIC, FULL_OPEN, PARTIAL_OPEN, ONE_WAY, LOCK
from common.kernel.core.BaseDataList import BaseDataList
from common.kernel.status.BaseStatus import BaseStatus

slidingStatusList = BaseDataList()
slidingStatusList.add(BaseStatus(2, AUTOMATIC, "images/sliding_automatic.png", None, default=True))  # "images/automatic.gif"
slidingStatusList.add(BaseStatus(1, FULL_OPEN, "images/sliding_fullopen.png", None, settingMode=True, is_open_status=True))  # "images/fullopen.gif"
slidingStatusList.add(BaseStatus(3, PARTIAL_OPEN, "images/sliding_partialopen.png", None))  # "images/partialopen.gif"
slidingStatusList.add(BaseStatus(5, ONE_WAY, "images/sliding_oneway.png", None))  # "images/oneway.gif"
slidingStatusList.add(BaseStatus(4, LOCK, "images/sliding_lock.png", None, is_locked_status=True))  # "images/lock.gif"
