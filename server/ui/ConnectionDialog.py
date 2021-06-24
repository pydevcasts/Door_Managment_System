from Globals import ini
from PyQtImports import QLabel, QRadioButton, QCheckBox
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CStatusBarDialog import CStatusBarDialog


class ConnectionDialog(CStatusBarDialog):


    ###########################################################################
    def __init__(self):
        CStatusBarDialog.__init__(self)

        tabSpace = "           "

        label = QLabel("Choose your connection:")
        self.addSingle(label)

        self.wifiRadioButton = QRadioButton("WiFi")
        self.wifiRadioButton.toggled.connect(lambda: self.connectionChanged(self.wifiRadioButton))
        self.addSingle(self.wifiRadioButton)

        self.projectText = CLineEdit()
        self.projectText.setMinimumSize(250, 25)
        self.addDouble(QLabel(tabSpace + "Project key"), self.projectText)

        self.webRadioButton = QRadioButton("Web")
        self.webRadioButton.toggled.connect(lambda: self.connectionChanged(self.webRadioButton))
        self.addSingle(self.webRadioButton)

        self.webServerText = CLineEdit()
        self.webServerText.setMinimumSize(250, 25)
        self.addDouble(QLabel(tabSpace + "Web Server"), self.webServerText)

        self.userNameText = CLineEdit()
        self.userNameText.setMinimumSize(250, 25)
        self.addDouble(QLabel(tabSpace + "User Name"), self.userNameText)

        self.passwordText = CLineEdit()
        self.passwordText.setMinimumSize(250, 25)
        self.addDouble(QLabel(tabSpace + "Password"), self.passwordText)

        self.rememberMe = QCheckBox("Remember my decision")
        self.addSingle(self.rememberMe)

        self.connectButton = self.addButton("Connect")
        self.connectButton.clicked.connect(self.connectClicked)

        self.cancelButton = self.addButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.statusListenTo(self.projectText)
        self.statusListenTo(self.webServerText)
        self.statusListenTo(self.userNameText)
        self.statusListenTo(self.passwordText)

    ######################################################
    def connectionChanged(self, currentRadioButton):
        self.projectText.setEnabled(self.wifiRadioButton.isChecked())
        self.webServerText.setEnabled(self.webRadioButton.isChecked())
        self.userNameText.setEnabled(self.webRadioButton.isChecked())
        self.passwordText.setEnabled(self.webRadioButton.isChecked())

    ###########################################################################
    def show(self):
        remember = ini.getConnectionRemember()
        self.rememberMe.setChecked(remember)

        self.wifiRadioButton.setChecked(remember and ini.getConnection() == "wifi")
        self.projectText.setText(ini.getProjectKey() if remember else "")

        self.webRadioButton.setChecked(remember and ini.getConnection() == "web")
        self.webServerText.setText(ini.getWebServer() if remember else "")
        self.userNameText.setText(ini.getWebUserName() if remember else "")
        self.passwordText.setText(ini.getWebPassword() if remember else "")

        CStatusBarDialog.show(self)

    ###########################################################################
    def cancelClicked(self):
        self.close()

    ###########################################################################
    def connectClicked(self):
        if self.wifiRadioButton.isChecked():
            if self.wifiClicked():
                self.close()
        elif self.webRadioButton.isChecked():
            if self.webClicked():
                self.close()

    ###########################################################################
    def wifiClicked(self):
        projectKey = ""
        if self.projectText.text() is not None:
            projectKey = str(self.projectText.text())

        from server.connection.ConnectionManager import connectionManager
        from server.wifi.WifiConnectionManager import WifiConnectionManager
        if not connectionManager.set(WifiConnectionManager(projectKey)):
            return False

        remember = self.rememberMe.isChecked()
        ini.setConnectionRemember(remember)
        ini.setConnection("wifi" if remember else "")
        ini.setProjectKey(projectKey if remember else "")
        ini.save()

        return True

    ###########################################################################
    def webClicked(self):
        webServer = str(self.webServerText.text())
        username = str(self.userNameText.text())
        password = str(self.passwordText.text())

        from server.connection.ConnectionManager import connectionManager
        from server.web.WebConnectionManager import WebConnectionManager
        if not connectionManager.set(WebConnectionManager(webServer, username, password)):
            self.setStatusText("Unable to connect to web server.")
            return False

        remember = self.rememberMe.isChecked()
        ini.setConnectionRemember(remember)
        ini.setConnection("web" if remember else "")
        ini.setWebServer(webServer if remember else "")
        ini.setWebUserName(username if remember else "")
        ini.setWebPassword(password if remember else "")
        ini.save()

        return True


###########################################################################################
###########################################################################################
###########################################################################################

connectionDialog = ConnectionDialog()
