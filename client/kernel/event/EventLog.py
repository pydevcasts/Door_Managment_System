from common.kernel.event.EventLog import EventLog as CommonEventLog
from client.kernel.analyze.Analyzer1000 import analyzer1000


class EventLog(CommonEventLog):
    """commoneventlog imported from common event"""
    def __init__(self, request=None, response=None):
        CommonEventLog.__init__(self, request, response)
        self.ping = analyzer1000.getLastPing()
        self.cycles = analyzer1000.getCycles()
