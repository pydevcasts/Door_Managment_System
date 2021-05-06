from Lang import lget, OK, CANCEL, ENTER_THE_NEW_VALUE_FOR_SETTING
from PyQtImports import Qt, QLabel
from common.shell.ui.dialog.CDialog import CDialog


class SettingInputDialog(CDialog):

    def __init__(self, settingWrapper):
        CDialog.__init__(self)

        self.settingWrapper = settingWrapper
        self.editor = settingWrapper.editor

        self.label = QLabel(lget(ENTER_THE_NEW_VALUE_FOR_SETTING, settingWrapper.getTitle()))
        self.addSingle(self.label)
        self.addSingle(self.editor)

        self.okButton = self.addButton(OK)
        self.okButton.clicked.connect(self.okClicked)

        self.cancelButton = self.addButton(CANCEL)
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.setWindowModality(Qt.ApplicationModal)

    def setTranslations(self):
        self.label.setText(lget(ENTER_THE_NEW_VALUE_FOR_SETTING, self.settingWrapper.getTitle()))
        self.editor.setTranslations()
        self.okButton.setTranslations()
        self.cancelButton.setTranslations()

    def okClicked(self):
        self.settingWrapper.inputDialogAccepted()
        self.close()

    def cancelClicked(self):
        self.close()
