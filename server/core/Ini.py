from common.kernel.Ini import Ini as CommonIni


class Ini(CommonIni):

    #############################################
    def __init__(self):
        CommonIni.__init__(self)

        self.ProjectKey = "DATA01"
        self.Connection = "DATA02"
        self.WebServer = "DATA03"
        self.WebUser = "DATA04"
        self.WebPassword = "DATA05"
        self.ConnectionRemember = "DATA06"

    #############################################
    def getFileName(self):
        return "cache/server-ini.bin"

    # Project Key
    #############################################
    def getProjectKey(self):
        return self.get(self.ProjectKey)

    def setProjectKey(self, projectKey):
        self.set(self.ProjectKey, projectKey)

    # Connection
    #############################################
    def getConnection(self):
        return self.get(self.Connection)

    def setConnection(self, connection):
        self.set(self.Connection, connection)

    # Web Server
    #############################################
    def getWebServer(self):
        return self.get(self.WebServer)

    def setWebServer(self, webServer):
        self.set(self.WebServer, webServer)

    # Web User
    #############################################
    def getWebUserName(self):
        return self.get(self.WebUser)

    def setWebUserName(self, webUser):
        self.set(self.WebUser, webUser)

    # Web Password
    #############################################
    def getWebPassword(self):
        return self.get(self.WebPassword)

    def setWebPassword(self, webPassword):
        self.set(self.WebPassword, webPassword)

    # Connection Remember
    #############################################
    def getConnectionRemember(self):
        return 'True' == self.get(self.ConnectionRemember)

    def setConnectionRemember(self, connectionRemember):
        self.set(self.ConnectionRemember, connectionRemember)
