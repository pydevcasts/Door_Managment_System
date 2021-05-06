from Globals import ini
from PyQtImports import QWidget, QScrollArea, QFrame, QGridLayout
from common.kernel.core.Role import *
from common.shell.ui.CLightButton import CLightButton
from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.dialog.CPasswordEditDialog import CPasswordEditDialog
from common.shell.ui.dialog.CTextInputDialog import CTextInputDialog
from server.connection.ConnectionManager import connectionManager


class PasswordsPanel(QWidget):

    ######################################################################################
    def __init__(self, doorPanel, role):
        QWidget.__init__(self)
        self.doorPanel = doorPanel

        outerLayout = QGridLayout(self)
        outerLayout.setContentsMargins(2, 2, 2, 2)
        outerLayout.setSpacing(0)
        outerLayout.setRowStretch(0, 1)
        outerLayout.setColumnStretch(0, 1)

        self.rowPanel = CRowPanel()
        scroll = QScrollArea()
        scroll.setWidget(self.rowPanel)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outerLayout.addWidget(scroll, 0, 0, 1, 1)

        from Lang import SET_USER_PASSWORD, SET_ADVANCED_USER_PASSWORD, SET_OWNER_PASSWORD, SET_INSTALLER_PASSWORD

        if role >= ROLE_OWNER:
            self.rowPanel.addSingle(
                CLightButton("   set Door Name    ", "images/door_name.png", 64, self.doorNameButtonClicked))

        if role >= ROLE_INSTALLER and connectionManager.get().getConnectionType() != connectionManager.CONNECTION_TYPE_WEB:
            self.rowPanel.addSingle(
                CLightButton("   set Project Key    ", "images/project_key.png", 64, self.projectKeyButtonClicked))

        if role >= ROLE_INSTALLER and connectionManager.get().getConnectionType() != connectionManager.CONNECTION_TYPE_WEB:
            self.rowPanel.addSingle(
                CLightButton("   set Web Server    ", "images/web.png", 64, self.webServerButtonClicked))

        if role >= ROLE_USER:
            self.rowPanel.addSingle(
                CLightButton(SET_USER_PASSWORD, "images/user.png", 64, self.userPasswordButtonClicked))

        if role >= ROLE_ADVANCED_USER:
            self.rowPanel.addSingle(CLightButton(SET_ADVANCED_USER_PASSWORD, "images/advanceduser.png", 64,
                                                 self.advancedPasswordButtonClicked))

        if role >= ROLE_OWNER:
            self.rowPanel.addSingle(
                CLightButton(SET_OWNER_PASSWORD, "images/owner.png", 64, self.ownerPasswordButtonClicked))

        if role >= ROLE_OWNER:
            self.rowPanel.addSingle(
                CLightButton(SET_INSTALLER_PASSWORD, "images/installer.png", 64, self.installerPasswordButtonClicked))

    ######################################################################################
    def userPasswordButtonClicked(self):
        self.passwordButtonClicked(ROLE_USER)

    ######################################################################################
    def advancedPasswordButtonClicked(self):
        self.passwordButtonClicked(ROLE_ADVANCED_USER)

    ######################################################################################
    def ownerPasswordButtonClicked(self):
        self.passwordButtonClicked(ROLE_OWNER)

    ######################################################################################
    def installerPasswordButtonClicked(self):
        self.passwordButtonClicked(ROLE_INSTALLER)

    ######################################################################################
    def passwordButtonClicked(self, role):
        dialog = CPasswordEditDialog()
        dialog.show()
        if not dialog.isAccepted():
            return

        oldPassword = dialog.getOldPassword()
        newPassword = dialog.getNewPassword()

        from common.kernel.request.SetPasswordRequest import SetPasswordRequest
        request = SetPasswordRequest(role, oldPassword, newPassword)
        response, exception = self.doorPanel.callRequest(request)

        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        self.doorPanel.alert("Password changed successfully.")

    ######################################################################################
    def doorNameButtonClicked(self):
        dialog = CTextInputDialog("Enter new Door Name:", defaultText=self.doorPanel.getDoor().name)
        dialog.show()
        if not dialog.isAccepted():
            return

        newName = dialog.getText()

        from common.kernel.request.SetNameRequest import SetNameRequest
        request = SetNameRequest(newName)
        response, exception = self.doorPanel.callRequest(request)

        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        self.doorPanel.alert("Door Name changed successfully.")

    ######################################################################################
    def webServerButtonClicked(self):
        dialog = CTextInputDialog("Enter web server URL:")
        dialog.show()
        if not dialog.isAccepted():
            return

        webServer = dialog.getText()

        from common.kernel.request.SetWebServerRequest import SetWebServerRequest
        request = SetWebServerRequest(webServer)
        response, exception = self.doorPanel.callRequest(request)

        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        self.doorPanel.alert("Web server saved successfully.")

    ######################################################################################
    def projectKeyButtonClicked(self):
        dialog = CTextInputDialog("Enter new Project Key:", defaultText=ini.getProjectKey())
        dialog.show()
        if not dialog.isAccepted():
            return

        newName = dialog.getText()

        from common.kernel.request.SetProjectRequest import SetProjectRequest
        request = SetProjectRequest(newName)
        response, exception = self.doorPanel.callRequest(request)

        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        self.doorPanel.alert("Project Key changed successfully.")
