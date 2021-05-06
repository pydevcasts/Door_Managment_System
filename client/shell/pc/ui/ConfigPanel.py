from Globals import interface, ini
from Lang import lget, lregister, OK, CANCEL
from PyQtImports import QMetaObject, pyqtSignal
from PyQtImports import QWidget, QGridLayout, QLabel
from client.shell.pc.PasswordManager import passwordManager
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.CPushButton import CPushButton
from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.Constants import Constants
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import darkGrayForeground


class ConfigPanel(CRowPanel):
    updateUISignal = pyqtSignal()

    ######################################################################################
    def __init__(self):
        CRowPanel.__init__(self)
        self.configList = []

        # Buttons
        self.buttonPanel = QWidget()
        self.addSingle(self.buttonPanel)

        self.buttonLayout = QGridLayout(self.buttonPanel)
        self.buttonLayout.setColumnStretch(0, 1)
        self.buttonLayout.setColumnStretch(3, 1)

        self.okButton = CPushButton(OK, clicked=self.okClicked)
        self.buttonLayout.addWidget(self.okButton, 0, 1, 1, 1)

        self.cancelButton = CPushButton(CANCEL, clicked=self.cancelClicked)
        self.buttonLayout.addWidget(self.cancelButton, 0, 2, 1, 1)

        QMetaObject.connectSlotsByName(self)
        self.updateUISignal.connect(self.updateUI)

        lregister(self)

        self.updateUI()

    ######################################################################################
    def setTranslations(self):
        self.okButton.setTranslations()
        self.cancelButton.setTranslations()
        for config in self.configList:
            config[3].setText(lget(config[4]))

    ######################################################################################
    def selectionAccepted(self):
        if not passwordManager.installerAccess():
            return False

        interface.get().setSettingMode(False)
        self.updateUI()
        return True

    ######################################################################################
    def addConfig(self, titleKey, getter, setter=None):
        label = self.createLabel(lget(titleKey))
        text = self.createLineEdit()
        if setter is None:
            text.setEnabled(False)
        self.addDouble(label, text)
        self.configList.append([text, getter, setter, label, titleKey])

    ######################################################################################
    def createLabel(self, text):
        label = QLabel(text)
        label.setMinimumSize(1, Constants.DEFAULT_EDITOR_HEIGHT)
        label.setMaximumSize(Constants.INFINITY_SIZE, Constants.DEFAULT_EDITOR_HEIGHT)
        label.setStyleSheet(darkGrayForeground())
        label.setFont(Fonts.LabelFont)
        return label

    ######################################################################################
    def createLineEdit(self):
        lineEdit = CLineEdit()
        lineEdit.textChanged.connect(self.textChanged)
        return lineEdit

    ######################################################################################
    def refreshUI(self):
        self.updateUISignal.emit()

    ######################################################################################
    def updateUI(self):
        for config in self.configList:
            text = config[0]
            getter = config[1]
            text.setText(getter())

        self.okButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

    ######################################################################################
    def textChanged(self, string):
        self.okButton.setEnabled(True)
        self.cancelButton.setEnabled(True)

    ######################################################################################
    def okClicked(self):
        for config in self.configList:
            text = config[0]
            setter = config[2]
            if setter is not None:
                setter(text.text())
        ini.save()
        self.updateUI()

    ######################################################################################
    def cancelClicked(self):
        self.updateUI()


##########################################################################################
##########################################################################################
##########################################################################################
configPanel = ConfigPanel()
