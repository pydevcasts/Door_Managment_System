from Globals import logger, ini
from Lang import lget
from common.kernel.core.Role import *
# from client.kernel.Ini import Ini as ini

DEFAULT_EMPTY = "__NO_PASSWORD__"
DEFAULT_USER = "0000"
DEFAULT_ADVANCED_USER = "0030"
DEFAULT_OWNER = "0049"
DEFAULT_INSTALLER = "3341"


class Authorizer:
    """get and set password reset password encryot impty valid password check password chech user chech 
    advance user"""
    def __init__(self):

        from Lang import USER, ADVANCED_USER, OWNER, INSTALLER

        self.roles = [
            (ROLE_USER, DEFAULT_USER, USER),
            (ROLE_ADVANCED_USER, DEFAULT_ADVANCED_USER, ADVANCED_USER),
            (ROLE_OWNER, DEFAULT_OWNER, OWNER),
            (ROLE_INSTALLER, DEFAULT_INSTALLER, INSTALLER)
        ]

        for roleTuple in self.roles:
            if ini.getPassword(roleTuple[0]) is None:
                ini.setPassword(roleTuple[0], self.encrypt(roleTuple[1]))

        ini.save()

    ###############################################################################
    def resetPasswords(self):
        for roleTuple in self.roles:
            ini.setPassword(roleTuple[0], self.encrypt(roleTuple[1]))
        ini.save()

    ###############################################################################
    def getText(self, role):
        for roleTuple in self.roles:
            if roleTuple[0] == role:
                return lget(roleTuple[2])

        from Lang import NO_ACCESS
        return lget(NO_ACCESS)

    ###############################################################################
    def encrypt(self, stringValue):
        if stringValue is None:
            return None

        stringValue = str(stringValue)

        import hashlib
        digest = hashlib.md5(stringValue.encode('utf-8')).hexdigest()
        return str(digest)

    ###############################################################################
    def isEmptyPassword(self, role):
        return ini.getPassword(role) == self.encrypt(DEFAULT_EMPTY)

    ###############################################################################
    def getRole(self, password):

        for roleTuple in reversed(self.roles):
            role = roleTuple[0]
            if self.isEmptyPassword(role):
                return role
            if self.encrypt(password) == ini.getPassword(role):
                return role

        return ROLE_NONE

    ###############################################################################
    def checkPassword(self, role, password):
        return self.getRole(password) == role

    ###############################################################################
    def checkAccess(self, role, password):
        return self.getRole(password) >= role

    ###############################################################################
    def checkUser(self, password):
        return self.checkAccess(ROLE_USER, password)

    ###############################################################################
    def checkAdvancedUser(self, password):
        return self.checkAccess(ROLE_ADVANCED_USER, password)

    ###############################################################################
    def checkOwner(self, password):
        return self.checkAccess(ROLE_OWNER, password)

    ###############################################################################
    def checkInstaller(self, password):
        return self.checkAccess(ROLE_INSTALLER, password)

    ###############################################################################
    def setPassword(self, role, password):
        ini.setPassword(role, self.encrypt(password))

    ###############################################################################
    def setUser(self, password):
        ini.setPassword(ROLE_USER, password)

    ###############################################################################
    def setAdvancedUser(self, password):
        ini.setPassword(ROLE_USER, password)

    ###############################################################################
    def setOwner(self, password):
        ini.setPassword(ROLE_ADVANCED_USER, password)

    ###############################################################################
    def setInstaller(self, password):
        ini.setPassword(ROLE_OWNER, password)

    ###############################################################################
    def setAdvancedUserPassword(self, password):
        ini.setPassword(ROLE_INSTALLER, password)

    ###############################################################################
    def checkDoorRequest(self, request):

        from client.kernel.core.DoorInfo import doorInfo

        try:
            if request.serial != doorInfo.getSerial():
                return False

        except:
            return False

        return self.checkProjectRequest(request)

    ###############################################################################
    def checkProjectRequest(self, request):

        from client.kernel.core.DoorInfo import doorInfo
        infoProject = doorInfo.getProject()
        if infoProject is None or infoProject == "":
            return True  
            # No project key cheking when we have defined project key on door-side

        try:
            requestProject = request.project
        except:
            import traceback
            logger.exception(traceback.format_exc())
            return False

        # Authorization check
        return requestProject == infoProject


################################################################################
################################################################################
################################################################################
authorizer = Authorizer()
