

####################################################################################
####################################################################################
class Command:

    ################################################################################
    def __init__(self, parameterCode, titleKey, imageAddress):
        self.parameterCode = parameterCode
        self.titleKey = titleKey
        self.imageAddress = imageAddress

    ################################################################################
    def getParameterCode(self):
        return self.parameterCode

    ################################################################################
    def getTitle(self):
        from Lang import lget
        return lget(self.titleKey)
        """ برگرداندن تابع
        def lget(key, *params):
            return language.get(key, *params)
        """

    ################################################################################
    def getImageAddress(self):
        return self.imageAddress

    ################################################################################
    def find(self, code):
        if self.parameterCode == code:
            return self
        return None

    ################################################################################
    def getPureSettingsList(self):
        return []
