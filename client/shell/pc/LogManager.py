from PyQtImports import QObject, pyqtSignal

"""PyQt"""
class LogManager(QObject):
    updateUiLog = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.maxCount = 100
        self.logs = []

    def logAdded(self, log):
        while len(self.logs) >= self.maxCount:
            self.logs = self.logs[1:]

        self.logs.append(log)
        self.updateUiLog.emit(self.getHtmlText())

    def getHtmlText(self):
        html = ""
        for log in self.logs:
            html = html + log + "<br/>"
        return html


########################################################################
########################################################################
########################################################################
########################################################################
logManager = LogManager()
