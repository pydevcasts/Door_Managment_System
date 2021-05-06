import threading

from client.kernel.analyze.Analyzer1000 import analyzer1000


class SerialSendQueue:

    #################################################
    def __init__(self):
        self.queue = []
        self.batch = None
        self.lock = threading.Lock()

        # Let first serial response to be a simple 3000
        self.add(analyzer1000.generateStatusList())

    #################################################
    def add(self, sendList):
        if sendList is None:
            return

        self.lock.acquire()
        # print("add: " + str(sendList))
        copy = sendList[0:sendList[1]]  # sendList.copy()
        self.queue.append(copy)
        self.queue.append(analyzer1000.generateStatusList())  # Let it Breath!
        self.lock.release()

    #################################################
    def remove(self):
        # print(str(len(self.queue)))
        if len(self.queue) <= 0:
            return None

        self.lock.acquire()
        sendList = self.queue[0]
        self.queue = self.queue[1:]
        self.lock.release()

        return sendList

    #################################################
    def addBatch(self, sendList):
        if self.batch is None:
            self.batch = []

        self.batch.append(sendList)

    #################################################
    def commitBatch(self):
        if self.batch is None:
            return

        size = len(self.batch)
        self.lock.acquire()
        # print("commit: " + str(self.batch))
        self.queue.extend(self.batch)
        self.batch = None
        self.lock.release()

        return size

    #################################################
    def rollbackBatch(self):
        self.batch = None


#################################################
#################################################
#################################################
serialSendQueue = SerialSendQueue()
