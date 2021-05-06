from Globals import interface
from Lang import lget, APPLICATION_TITLE
from PyQtImports import QIcon
from PyQtImports import QMainWindow, QWidget, QDesktopWidget, QGridLayout, QScrollArea, QLabel, QToolBar, QToolButton
from PyQtImports import QMetaObject, QSize, pyqtSignal
from client.shell.admin.data.Database import database
from client.shell.admin.editor.EditorFactory import editorFactory
from client.shell.admin.ui.ProfileWidget import ProfileWidget
from client.shell.admin.ui.RequestWaitDialog import RequestWaitDialog
from client.shell.admin.ui.SerialDialog import SerialDialog
from common.kernel.request.CommandRequest import CommandRequest
from common.kernel.request.DoorRequest import DoorRequest
from common.kernel.setting.Setting import Setting
from common.kernel.setting.SettingsPack import SettingsPack
from common.shell.ui.CAppHeader import CAppHeader
from common.shell.ui.CRowLayout import CRowLayout
from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.CTitle import CTitle
from common.shell.ui.Fonts import Fonts
from common.shell.ui.dialog.CAlertDialog import CAlertDialog
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog
from common.shell.ui.dialog.CTextInputDialog import CTextInputDialog


class MainWindow(QMainWindow):
    profileToUiSignal = pyqtSignal(dict)
    updateUiSignal = pyqtSignal()
    deleteProfileSignal = pyqtSignal(str)

    #######################################################################################
    def __init__(self):

        QMainWindow.__init__(self)

        self.labelFont = Fonts.createFont(Fonts.FAMILY_ARIAL, 10, False, False)
        self.headerFont = []
        for i in range(0, 3):
            self.headerFont.append(Fonts.createFont(Fonts.FAMILY_ARIAL, (30 - 9 * i), False, False))

        self.settingMap = {}

        self.currentProfileName = None
        self.changed = False

        self.setWindowTitle(lget(APPLICATION_TITLE))

        from common.shell.AppIcon import appIcon
        self.setWindowIcon(appIcon)

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.header = CAppHeader()
        panel = self.header.install(self, self.centralwidget)

        self.gridLayout = QGridLayout(panel)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setColumnStretch(0, 1)

        self.profileText = CTitle("Unknown")
        self.gridLayout.addWidget(self.profileText, 0, 0, 1, 1)

        self.createToolbar()

        self.createSettingPanel()

        self.createEastPanel()

        # self.logWidget = QTextEdit()
        # self.logWidget.setReadOnly(True)
        # self.gridLayout.addWidget(self.logWidget, 2, 0, 1, 2)

        self.setFixedSize(1000, 800)

        QMetaObject.connectSlotsByName(self)

        self.loadData()

        QMetaObject.connectSlotsByName(self)
        self.profileToUiSignal.connect(self.profileToUi)
        self.updateUiSignal.connect(self.updateUiSlot)
        self.deleteProfileSignal.connect(self.deleteProfileSlot)

        self.newButtonClicked()

        # logManager.updateUiLog.connect(self.updateLogs)
        # self.updateLogs(logManager.getHtmlText())

    #######################################################################################
    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        w = (resolution.width() / 2) - (self.frameSize().width() / 2)
        h = (resolution.height() / 2) - (self.frameSize().height() / 2)
        self.move(w, h)

    #######################################################################################
    def show(self):
        self.centerOnScreen()
        QMainWindow.show(self)

    #######################################################################################
    def closeEvent(self, event):
        QMainWindow.closeEvent(self, event)

    #######################################################################################
    # def updateLogs(self, htmlText):
    #    self.logWidget.clear()
    #    self.logWidget.textCursor().insertHtml(htmlText)
    #    self.logWidget.moveCursor(QtGui.QTextCursor.End)

    #######################################################################################
    # def loginTextUpdate(self):
    #    from client.shell.pc.PasswordManager import passwordManager
    #    self.loginStatus.setText("            " + passwordManager.getLoginText())

    #######################################################################################
    def validateProfileName(self):
        if self.currentProfileName is not None:
            return self.currentProfileName
        return "Unknown"

    #######################################################################################
    def updateUI(self):
        self.updateUiSignal.emit()

    #######################################################################################
    def updateUiSlot(self):
        profileName = self.validateProfileName()

        exist = (self.currentProfileName is not None)

        if self.changed:
            profileName = profileName + "*"

        self.profileText.setText(profileName)

        self.ignoreButton.setEnabled(self.changed)
        self.newButton.setEnabled(not self.changed)
        self.saveButton.setEnabled(exist and self.changed)
        self.saveAsButton.setEnabled(self.changed)

        self.readSettingButton.setEnabled(not self.changed)
        self.applySettingButton.setEnabled(not self.changed)
        self.initializeSetupButton.setEnabled(not self.changed)
        self.factoryDefaultsButton.setEnabled(not self.changed)
        self.userDefaultsButton.setEnabled(not self.changed)
        self.saveUserDefaultsButton.setEnabled(not self.changed)

    #######################################################################################
    def valueChanged(self, editor):
        self.changed = True
        self.updateUI()

    #######################################################################################
    def createToolbar(self):
        # northPanel = QtGui.QWidget()
        # self.gridLayout.addWidget(northPanel, 1, 0, 1, 1)
        # northLayout = QtGui.QGridLayout(northPanel)
        # northLayout.setColumnStretch(1, 1)

        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet('QToolBar{spacing:10px;}')
        self.toolbar.setIconSize(QSize(48, 48))
        self.gridLayout.addWidget(self.toolbar, 1, 0, 1, 1)
        # northLayout.addWidget(toolbar, 0, 0, 1, 1)
        # toolbarLayout = QtGui.QHBoxLayout(toolbar)

        self.ignoreButton = self.addToolbarButton('images/ignore48.png', "Ignore", self.ignoreButtonClicked)

        self.newButton = self.addToolbarButton('images/new48.png', "New Profile (Factory Defaults)",
                                               self.newButtonClicked)

        self.saveButton = self.addToolbarButton('images/save48.png', "Save", self.saveButtonClicked)

        self.saveAsButton = self.addToolbarButton('images/saveas48.png', "Save As", self.saveAsButtonClicked)

        self.toolbar.addSeparator()

        self.readSettingButton = self.addToolbarButton('images/read48.png', "Load Door Settings", self.readSettings)

        self.applySettingButton = self.addToolbarButton('images/write48.png', "Apply Settings to Door",
                                                        self.applySettings)

        self.toolbar.addSeparator()

        self.initializeSetupButton = self.addToolbarButton('images/init48.png', "Initialize Setup",
                                                           self.initializeSetup)

        self.factoryDefaultsButton = self.addToolbarButton('images/factory48.png', "Revert To Factory Defaults",
                                                           self.revertToFactoryDefaults)

        self.userDefaultsButton = self.addToolbarButton('images/loaddefault48.png', "Revert To User Defaults",
                                                        self.revertToUserDefaults)

        self.saveUserDefaultsButton = self.addToolbarButton('images/savedefault48.png', "Save as User Defaults",
                                                            self.saveAsUserDefaults)

        self.setSerialButton = self.addToolbarButton('images/serial48.png', "Serial Number", self.setSerialNo)

    #######################################################################################
    def addToolbarButton(self, iconAddress, setToolTip, clickHandler):
        button = QToolButton()
        button.setIcon(QIcon(iconAddress))
        button.setToolTip(setToolTip)
        button.setAutoRaise(True)
        button.setIconSize(QSize(48, 48))
        button.clicked.connect(clickHandler)
        self.toolbar.addWidget(button)
        return button

    #######################################################################################
    def createSettingPanel(self):
        self.settingPanel = CRowPanel()
        scroll = QScrollArea()
        scroll.setWidget(self.settingPanel)
        scroll.setWidgetResizable(True)
        # scroll.setFrameShape (QtGui.QFrame.NoFrame)
        self.gridLayout.addWidget(scroll, 2, 0, 1, 1)

        settings, advancedSettings = interface.get().getSettings()
        self.addSetting(settings)
        self.addSetting(advancedSettings)

    #######################################################################################
    def addSetting(self, setting, depth=0):

        if isinstance(setting, Setting):

            if self.settingMap.get(setting.getParameterCode(), None) is not None:
                return

            label = QLabel((" " * 20) + setting.getTitle())
            label.setFont(self.labelFont)
            editor = editorFactory.getEditor(setting)
            editor.addValueChangeListener(self)
            self.settingMap[setting.getParameterCode()] = (setting, editor)
            self.settingPanel.addDouble(label, editor)

        elif isinstance(setting, SettingsPack):
            label = QLabel(setting.getTitle())  # ( " " * 3 * depth ) +
            label.setFont(self.headerFont[depth])
            self.settingPanel.addSingle(QLabel(" "))
            self.settingPanel.addSingle(label)
            for s in setting.settingList:
                self.addSetting(s, depth + 1)

    #######################################################################################
    def createEastPanel(self):
        eastPanel = QWidget()
        eastLayout = CRowLayout(eastPanel)
        eastLayout.setRowStretch(0, 1)
        self.gridLayout.addWidget(eastPanel, 0, 1, 3, 1)

        self.profilePanel = CRowPanel()
        eastLayout.addSingle(self.profilePanel)

        profileLabel = QLabel("Profiles:   ")
        profileLabel.setFont(Fonts.GroupTitleFont)
        profileLabel.setMinimumSize(200, 37)
        self.profilePanel.addSingle(profileLabel)

    #######################################################################################
    def addProfile(self, profileName):
        widget = ProfileWidget(self, profileName)
        self.profileWidgets.append(widget)
        self.profilePanel.addSingle(widget)

    #######################################################################################
    def loadData(self):
        self.profileWidgets = []
        profileList = database.getProfiles()
        for profile in profileList:
            self.addProfile(profile["name"])

    #######################################################################################
    def loadProfile(self, profileName):
        if not self.checkForSave():
            return

        profile = database.get(profileName)

        self.currentProfileName = profile["name"]

        self.profileToUiSignal.emit(profile)

    #######################################################################################
    def deleteProfile(self, profileName):
        if not self.checkForSave():
            return

        dialog = CQuestionDialog("Are you sure you want to delete " + profileName + "?")
        dialog.show()
        if not dialog.isAccepted():
            return

        if database.delete(profileName):
            self.deleteProfileSignal.emit(profileName)

    #######################################################################################
    def deleteProfileSlot(self, profileName):
        for widget in self.profileWidgets:
            if widget.profileName == profileName:
                self.profilePanel.layout.removeWidget(widget)
                widget.setParent(None)
                return

    #######################################################################################
    def profileToUi(self, profile):
        for key, tupple in self.settingMap.items():
            setting, editor = tupple
            value = profile.get(str(key), None)
            if value is not None:
                editor.setValue(value)

        self.changed = False
        self.updateUI()

    #######################################################################################
    def createUiProfile(self):
        uiProfile = {"name": self.currentProfileName}

        for key, value in self.settingMap.items():
            setting, editor = value
            uiProfile[str(setting.getParameterCode())] = editor.getValue()

        return uiProfile

    #######################################################################################
    def checkForSave(self):
        if not self.changed:
            return True

        dialog = CQuestionDialog("Save Changes to " + self.validateProfileName() + "?")
        dialog.show()

        if not dialog.isAccepted():
            return False

        if self.currentProfileName is not None:
            return self.saveButtonClicked()

        return self.saveAsButtonClicked()

    #######################################################################################
    def ignoreButtonClicked(self):
        self.changed = False
        if self.currentProfileName is None:
            self.newButtonClicked()
        else:
            self.loadProfile(self.currentProfileName)

    #######################################################################################
    def newButtonClicked(self):
        if not self.checkForSave():
            return

        self.currentProfileName = None

        for key, value in self.settingMap.items():
            setting, editor = value
            editor.setValue(setting.getFactoryDefault())

        self.changed = False
        self.updateUI()

    #######################################################################################
    def saveButtonClicked(self):
        if self.currentProfileName is None:
            return self.saveAsButtonClicked()

        if not self.changed:
            return True

        newProfile = self.createUiProfile()

        newProfileName = database.update(newProfile)

        if newProfileName != self.currentProfileName:
            self.addProfile(newProfileName)

        self.changed = False
        self.loadProfile(newProfileName)

        return True

    #######################################################################################
    def saveAsButtonClicked(self):
        if not self.changed:
            return True

        dialog = CTextInputDialog("New Profile Name:            ")
        dialog.show()

        if not dialog.isAccepted():
            return False

        newProfile = self.createUiProfile()
        newProfile["name"] = dialog.getText()

        newProfileName = database.add(newProfile)

        self.changed = False
        self.addProfile(newProfileName)
        self.loadProfile(newProfileName)

        return True

    #######################################################################################
    def loadDoorValues(self):
        request = DoorRequest()
        response = interface.get().handle(request)

        dummyProfile = {}
        for key, value in response.params.items():
            dummyProfile[str(key)] = value

        self.currentProfileName = None
        self.changed = False
        dummyProfile["name"] = self.validateProfileName()

        self.profileToUiSignal.emit(dummyProfile)
        self.updateUI()

    #######################################################################################
    def readSettings(self):
        if not self.checkForSave():
            return

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        self.loadDoorValues()

    #######################################################################################
    def applySettings(self, showDialog=True):
        if not self.checkForSave():
            return

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        params = {}
        for key, value in self.settingMap.items():
            setting, editor = value
            params[key] = editor.getValue()

        from common.kernel.request.SetParamsRequest import SetParamsRequest
        request = SetParamsRequest(params)

        dialog = RequestWaitDialog(request)
        self.loadDoorValues()

        if showDialog:
            CAlertDialog("All Settings are applied to door.").show()

    #######################################################################################
    def initializeSetup(self):
        if not self.checkForSave():
            return

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        request = CommandRequest(3020)
        dialog = RequestWaitDialog(request)
        response = dialog.response

        CAlertDialog("Door is initialized.").show()

    #######################################################################################
    def revertToFactoryDefaults(self):
        if not self.checkForSave():
            return

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        request = CommandRequest(3021)
        dialog = RequestWaitDialog(request)
        response = dialog.response

        self.loadDoorValues()

        dialog = CQuestionDialog("Factory Settings are loaded. It is highly recommanded to run Initialize Setup. run?")
        dialog.show()
        if dialog.isAccepted():
            self.initializeSetup()

    #######################################################################################
    def revertToUserDefaults(self):
        if not self.checkForSave():
            return

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        request = CommandRequest(3094)
        dialog = RequestWaitDialog(request)
        response = dialog.response

        self.loadDoorValues()

        dialog = CQuestionDialog("Default values are loaded. It is highly recommanded to run Initialize Setup. run?")
        dialog.show()
        if dialog.isAccepted():
            self.initializeSetup()

    #######################################################################################
    def saveAsUserDefaults(self):
        if not self.checkForSave():
            return

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        self.applySettings(False)

        request = CommandRequest(3093)
        dialog = RequestWaitDialog(request)

        self.loadDoorValues()

        CAlertDialog("All Settings are applied to door and saved as user defaults.").show()

    #######################################################################################
    def setSerialNo(self):

        if not interface.get().isSerialConnected():
            CAlertDialog("Door is not connected").show()
            return

        dialog = SerialDialog()
        dialog.show()

        if not dialog.ok:
            return

        serial = dialog.getSerial()
        request = CommandRequest(3095)
        request.addProperty("serial", serial)
        dialog = RequestWaitDialog(request)

        response = dialog.response

        if response.accepted:
            CAlertDialog("The new Serial Number saved successfully.").show()
        else:
            CAlertDialog("Faild to save new Serial Number.").show()


############################################################
############################################################
############################################################
mainWindow = MainWindow()
