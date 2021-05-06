import threading
import time

from client.kernel.core.Authorizer import authorizer
from common.kernel.core.Role import *


class PasswordManager(threading.Thread):

    ###############################################################################
    def __init__(self):

        threading.Thread.__init__(self, name="PasswordManager")

        self.setDaemon(True)

        # Constants
        self.RolePeriod = (60 * 14) + 59  # a second less than 15 minutes
        self.expire = 0

        self.password = None

    ###############################################################################
    def access(self, role):
        if authorizer.getRole(self.password) >= role:
            return True

        from client.shell.pc.ui.PasswordDialog import PasswordDialog
        passwordDialog = PasswordDialog()
        passwordDialog.show(role)

        if passwordDialog.isAccepted():
            self.acceptPassword(passwordDialog.password)
            return True

        return False

    ###############################################################################
    def userAccess(self):
        return self.access(ROLE_USER)

    ###############################################################################
    def advancedUserAccess(self):
        return self.access(ROLE_ADVANCED_USER)

    ###############################################################################
    def ownerAccess(self):
        return self.access(ROLE_OWNER)

    ###############################################################################
    def installerAccess(self):
        return self.access(ROLE_INSTALLER)

    ###############################################################################
    def fillRequest(self, request, password=None):

        if request is None:
            return

        if password is None:
            password = self.password
        request.password = password

        from client.kernel.core.DoorInfo import doorInfo
        request.project = doorInfo.getProject()
        request.serial = doorInfo.getSerial()

    ###############################################################################
    def getLoginText(self):

        from Lang import lget, CURRENT_ACCESS, EXPIRES_IN, EXPIRES_IN_MINUTES

        role = authorizer.getRole(self.password)
        result = lget(CURRENT_ACCESS) + ": " + authorizer.getText(role)

        if role == ROLE_NONE:
            return result

        delta = self.expire - int(time.time())

        minutes = int(delta / 60)
        # print(lget(EXPIRES_IN_MINUTES))
        if minutes > 0:
            return result + " - " + lget(EXPIRES_IN_MINUTES, minutes + 1)

        seconds = str(delta % 60)
        if delta % 60 < 10:
            seconds = "0" + seconds

        return result + " - " + lget(EXPIRES_IN, "00:" + seconds)

    ###############################################################################
    def acceptPassword(self, password):
        self.password = str(password)
        self.expire = int(time.time() + self.RolePeriod)

    ###############################################################################
    def run(self):

        from client.shell.pc.ui.MainWindow import mainWindow

        t = time.time()

        while True:
            now = time.time()
            delta = int(now - t)
            if abs(delta) > 60:
                self.expire = self.expire + delta

            if self.expire <= now:
                self.password = None
                self.expire = 0

            t = now

            mainWindow.updateLoginText(self.getLoginText())
            time.sleep(0.3)


###############################################################################
###############################################################################
passwordManager = PasswordManager()
