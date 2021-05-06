from client.shell.pc.ui.PasswordEditDialog import PasswordEditDialog
from common.kernel.core.Role import *
from common.shell.ui.CLightButton import CLightButton
from common.shell.ui.CRowPanel import CRowPanel


class PasswordsPanel(CRowPanel):

    ######################################################################################
    def __init__(self):
        CRowPanel.__init__(self)

        from Lang import SET_USER_PASSWORD, SET_ADVANCED_USER_PASSWORD, SET_OWNER_PASSWORD, SET_INSTALLER_PASSWORD

        self.addPasswordPack("images/user.png", SET_USER_PASSWORD, self.userPasswordButtonClicked)
        self.addPasswordPack("images/advanceduser.png", SET_ADVANCED_USER_PASSWORD, self.advancedPasswordButtonClicked)
        self.ownerButton = self.addPasswordPack("images/owner.png", SET_OWNER_PASSWORD, self.ownerPasswordButtonClicked)
        self.InstallerButton = self.addPasswordPack("images/installer.png", SET_INSTALLER_PASSWORD,
                                                    self.installerPasswordButtonClicked)

    ######################################################################################
    def selectionAccepted(self):
        from client.shell.pc.ui.PasswordDialog import PasswordDialog
        from common.kernel.core.Role import ROLE_ADVANCED_USER, ROLE_OWNER, ROLE_INSTALLER
        from client.kernel.core.Authorizer import authorizer

        passwordDialog = PasswordDialog()
        passwordDialog.show(ROLE_ADVANCED_USER)

        if not passwordDialog.isAccepted():
            return False

        from Globals import interface
        interface.get().setSettingMode(False)

        role = authorizer.getRole(passwordDialog.password)
        self.ownerButton.setVisible(role >= ROLE_OWNER)
        self.InstallerButton.setVisible(role >= ROLE_INSTALLER)

        return True

    ######################################################################################
    def userPasswordButtonClicked(self):
        PasswordEditDialog(ROLE_USER).show()

    ######################################################################################
    def advancedPasswordButtonClicked(self):
        PasswordEditDialog(ROLE_ADVANCED_USER).show()

    ######################################################################################
    def ownerPasswordButtonClicked(self):
        PasswordEditDialog(ROLE_OWNER).show()

    ######################################################################################
    def installerPasswordButtonClicked(self):
        PasswordEditDialog(ROLE_INSTALLER).show()

    ######################################################################################
    def addPasswordPack(self, imageAddress, buttonText, buttonClickHandler):
        button = CLightButton(buttonText, imageAddress, 64, buttonClickHandler, translated=True)
        self.addSingle(button)

        return button


##########################################################################################
##########################################################################################
##########################################################################################
passwordsPanel = PasswordsPanel()
