import threading
from datetime import datetime


####################################################################################
####################################################################################
class Log:
    """debug error warning shit success"""
    ############################################################################
    def __init__(self, logType, text, *params):
        from Lang import lget
        self.text = lget(str(text), *params)
        self.logType = logType
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ############################################################################
    def __str__(self):
        return str(self.time) + " --- " + str(self.text)


####################################################################################
####################################################################################
class Logger:
    """debug error warning shit success"""
    TYPE_ERROR = 0
    TYPE_WARNING = 1
    TYPE_SUCCESS = 2
    TYPE_INFO = 3
    TYPE_EXCEPTION = 4
    TYPE_DEVELOP = 5
    TYPE_DEBUG = 6
    TYPE_SHIT = 7

    ############################################################################
    def __init__(self):
        self.logListeners = []

        from common.kernel.SysArgument import sysArgument
        self.fileLogEnabled = sysArgument.exists("FileLog")
        self.logLevel = sysArgument.getInt("LogLevel", Logger.TYPE_INFO)

        self.fileName = None
        self.logCounter = 0
        self.logBuffer = []

        self.lock = threading.Lock()

        from Exit import exit
        exit.register(self.cleanUp)

    ############################################################################
    def error(self, text, *params):
        self.addLog(Logger.TYPE_ERROR, text, *params)

    ############################################################################
    def warning(self, text, *params):
        self.addLog(Logger.TYPE_WARNING, text, *params)

    ############################################################################
    def success(self, text, *params):
        self.addLog(Logger.TYPE_SUCCESS, text, *params)

    ############################################################################
    def info(self, text, *params):
        self.addLog(Logger.TYPE_INFO, text, *params)

    ############################################################################
    def exception(self, text, *params):
        self.addLog(Logger.TYPE_EXCEPTION, text, *params)

    ############################################################################
    def develop(self, text, *params):
        self.addLog(Logger.TYPE_DEVELOP, text, *params)

    ############################################################################
    def debug(self, text, *params):
        self.addLog(Logger.TYPE_DEBUG, text, *params)

    ############################################################################
    def shit(self, text, *params):
        self.addLog(Logger.TYPE_SHIT, text, *params)

    ############################################################################
    def addLog(self, logType, text, *params):
        if self.logLevel < logType:
            return

        self.logCounter += 1

        log = Log(logType, text, *params)
        self.fireLogAdded(str(log))

    ############################################################################
    def addLogListener(self, listener):
        if listener is None:
            return
        self.logListeners.append(listener)

    ############################################################################
    def fireLogAdded(self, log):

        if self.logLevel >= Logger.TYPE_EXCEPTION:
            try:
                print(log)
            except:
                pass

        if self.fileLogEnabled:
            self.file(log)

        for listener in self.logListeners:
            listener.logAdded(log)

    ############################################################################
    def file(self, log):

        self.logBuffer.append(log)

        if len(self.logBuffer) < 5:
            return

        self.writeToFile()

    ############################################################################
    def writeToFile(self):

        self.lock.acquire()

        try:
            if len(self.logBuffer) == 0:
                return

            if self.fileName is None or self.logCounter % 1000 == 0:
                self.fileName = "log/DL " + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".txt"
                file = open(self.fileName, "w")
            else:
                file = open(self.fileName, "a")

            for log in self.logBuffer:
                file.write(str(log) + "\n")

            self.logBuffer = []
            file.close()

        except:
            import traceback
            # DO NOT USE LOGGER! Avoid infinite loop
            if self.logLevel >= Logger.TYPE_DEVELOP:
                print(traceback.format_exc())

        finally:
            self.lock.release()

    ############################################################################
    def cleanUp(self):
        self.writeToFile()
