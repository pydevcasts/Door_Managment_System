import subprocess
import time
import traceback

from Globals import logger


class RunTime:

    ##############################################################
    def __init__(self):
        pass

    ##############################################################
    def call(self, args, sleepTime=0):
        try:
            subprocess.call(args)
            if sleepTime > 0:
                time.sleep(sleepTime)
        except:
            logger.error(traceback.format_exc())

    ##############################################################
    def execute(self, args, sleepTime=0):
        try:
            str = subprocess.check_output(args)
            if sleepTime > 0:
                time.sleep(sleepTime)
            return str
        except:
            logger.error(traceback.format_exc())

        return None

    ##############################################################
    def script(self, fileName, *scriptArgs):
        try:
            args = ["sh", "scripts/" + fileName + ".sh"]
            args += scriptArgs
            subprocess.call(args)
        except:
            logger.error(traceback.format_exc())


##################################################################
##################################################################
##################################################################
runTime = RunTime()
