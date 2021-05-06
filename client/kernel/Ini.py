from common.kernel.Ini import Ini as CommonIni


class Ini(CommonIni):
    """set and get atrributes in this class
        [licenseKey,PasswordKey,DoorStatusKey,ServerHostKey,ProjectKey
        WebServerKey,LanguageKey ]
    Args:
        CommonIni :[ برای دی کد کردن کدهای جیسان و ذخیره ان,
         برای اند کد کردن  و لود شدن کدهای جیسان و نمایش در پایتون]
    """
    def __init__(self):
        CommonIni.__init__(self)

        self.LscKey = "DATA08"
        self.DoorStatusKey = "DATA04"

        self.PasswordKey = "DATA01"

        self.ServerHostKey = "DATA05"
        self.DoorNameKey = "DATA06"

        self.ProjectKey = "DATA10"

        self.WebServerKey = "DATA11"

        self.LanguageKey = "DATA12"

    def getFileName(self):
        return "cache/client-ini.bin"

    # Door Status
    #############################################
    def getDoorStatus(self):
        return self.getInt(self.DoorStatusKey)

    def setDoorStatus(self, doorStatus):
        self.set(self.DoorStatusKey, doorStatus)

    # Lsc
    #############################################
    def getLsc(self):
        return self.get(self.LscKey)

    def setLsc(self, lsc):
        self.set(self.LscKey, lsc)

    # Password
    #############################################
    def getPassword(self, role):
        return self.get(self.PasswordKey + "_" + str(role))

    def setPassword(self, role, password):
        self.set(self.PasswordKey + "_" + str(role), password)

    # Server Host
    #############################################
    def getServerHost(self):
        return self.get(self.ServerHostKey)

    def setServerHost(self, serverHost):
        self.set(self.ServerHostKey, serverHost)

    # Door Name
    #############################################
    def getDoorName(self):
        return self.get(self.DoorNameKey)

    def setDoorName(self, doorName):
        self.set(self.DoorNameKey, doorName)

    # Project
    #############################################
    def getProject(self):
        return self.get(self.ProjectKey)

    def setProject(self, project):
        self.set(self.ProjectKey, project)

    # Web Server Url
    #############################################
    def getWebServerUrl(self, defaultUrl=None):
        return self.get(self.WebServerKey, defaultUrl)

    def setWebServerUrl(self, url):
        self.set(self.WebServerKey, url)

    # Web Server Url
    #############################################
    def getLanguage(self):
        return self.get(self.LanguageKey)

    def setLanguage(self, lang):
        self.set(self.LanguageKey, lang)
