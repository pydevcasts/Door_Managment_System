class Reader:
    """to read serial received bytes carefully"""

    def __init__(self):
        self.dataList = [0, 3]
        self.reset()
        self.threshold = 50  # Maximum length

    def reset(self):
        self.dataList[0] = 0
        self.dataList[1] = 3
        self.index = 0

    def read(self, b):

        while self.index >= len(self.dataList):
            self.dataList.append(0)

        self.dataList[self.index] = b

        # to prevent some errors
        if self.dataList[1] < 3 or self.dataList[1] > self.threshold:
            self.reset()
            return

        # to prevent some errors
        if self.index > self.threshold:
            self.reset()
            return

        if self.dataList[0] != 0x80:
            self.reset()
            return

        self.index = self.index + 1
        if self.index >= self.dataList[1]:
            result = self.dataList[0: self.dataList[1]]
            self.reset()
            return result

        return None
