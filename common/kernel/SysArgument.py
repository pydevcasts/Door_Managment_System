import getopt
import sys


class SysArgument:

    ##########################################################################
    def __init__(self):
        try:
            options = ""  # no short option, example of usage : "hi:" - so "-h" and "-i <value>" will be valid options
            long_options = ["ConfigPanel", "FileLog",
                            "LogLevel="]  # so "--ConfigPanel" will be a valid option. this list might be extended in future
            opts, args = getopt.getopt(sys.argv[1:], options, long_options)
        except getopt.GetoptError:
            print("Error! Invalid application arguments.")
            sys.exit(2)

        # the following lines are commented as I need fully validated arguments, not arbitrary ones. so I only use opts
        # for arg in args :
        #    self.paramSet.add(arg.lower())

        self.paramDict = {}
        for key, value in opts:
            key = key.lower()
            if key[:2] == "--":
                key = key[2:]
            if key[:1] == "-":
                key = key[1:]
            self.paramDict[key] = value

            sys.argv = sys.argv[0:1]  # clear sys.argv because of dumb libraries such as webPy

    ##########################################################################
    def exists(self, param):
        return param is not None and param.lower() in self.paramDict

    ##########################################################################
    def get(self, key):
        return key is not None and self.paramDict.get(key.lower(), None)

    ##########################################################################
    def getInt(self, key, default):
        try:
            return int(self.get(key))
        except:
            return int(default)


##############################################################################
##############################################################################
##############################################################################
sysArgument = SysArgument()
