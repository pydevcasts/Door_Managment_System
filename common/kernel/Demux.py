class Demux:
    """frame"""

    ############################################################################
    def __init__(self):
        self.map = {}
        self.getPackage = None

    ############################################################################
    def register(self, obj):
        if obj is None:
            return

        className = obj.__module__
        index = className.rfind('.')
        packageName = className[:index]
        self.map[packageName] = obj

    ############################################################################
    def get(self):
        if self.getPackage is None:
            arr = [self.getPackage1, self.getPackage2, self.getPackage3]
            for getPackage in arr:
                try:
                    if getPackage() is not None:
                        self.getPackage = getPackage
                        break
                except:
                    pass

        package = self.getPackage()
        for key, value in self.map.items():
            if package.startswith(key):
                return value

        return None

    ############################################################################
    def getPackage1(self):  # frame Mode. works fine, but won't work in windows exe
        import sys
        package = sys._getframe(2).f_globals['__package__']
        return package

    ############################################################################
    def getPackage2(self):  # frame Mode, for windows executable
        import sys
        package = sys._getframe(2).f_globals['__spec__'].name
        return package

    ############################################################################
    def getPackage3(self):  # inspect mode. works fine, but won't work in windows exe
        import inspect
        frm = inspect.stack()[2]
        # [FrameInfo(frame=<frame at 0x000001D2395721D0, file '<stdin>', line 1, 
        # code <module>>, filename='<stdin>', lineno=1, function='<module>', code_context=None, index=None)]
        mod = inspect.getmodule(frm[0])
        package = mod.__name__
        return package

