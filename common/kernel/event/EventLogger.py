import time
import threading


class EventLogger:

    VALID_PERIOD = 120 * 60

    def __init__(self):
        self.events = []
        self.lock = threading.Lock()

    def add(self, event):
        if event is None:
            return
        self.lock.acquire()
        self.events.append(event)

        nowSeconds = int(round(time.time()))
        while len(self.events) > 100 and (nowSeconds - self.events[0].nowSeconds) > EventLogger.VALID_PERIOD :
            self.events = self.events[1:]

        self.lock.release()

    def removeAll(self):
        self.lock.acquire()
        result = self.events[:]

        nowSeconds = int(round(time.time()))
        for event in result:
            event.diffSeconds = nowSeconds - event.nowSeconds

        self.events = []
        self.lock.release()
        return result

    def push(self, events):
        if events is None or len(events) == 0:
            return

        self.lock.acquire()

        self.events = events + self.events

        nowSeconds = int(round(time.time()))
        while len(self.events) > 100 and (nowSeconds - self.events[0].nowSeconds) > EventLogger.VALID_PERIOD :
            self.events = self.events[1:]

        self.lock.release()


#########################################################
#########################################################
#########################################################
eventLogger = EventLogger()
