from Globals import ini, logger
from PyQtImports import QLabel
from common.shell.ui.CLineEdit import CLineEdit
from common.shell.ui.dialog.CStatusBarDialog import CStatusBarDialog


class ProjectDialog(CStatusBarDialog):

    ###########################################################################
    def __init__(self):
        CStatusBarDialog.__init__(self)

        self.label = QLabel("Enter Project Key:")

        self.textBox = CLineEdit()
        self.textBox.setMinimumSize(250, 25)
        self.textBox.setPlaceholderText("Enter project key here")

        self.addDouble(self.label, self.textBox)

        self.okButton = self.addButton("OK")
        self.okButton.clicked.connect(self.okClicked)

        self.cancelButton = self.addButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelClicked)

        self.statusListenTo(self.textBox)

    ###########################################################################
    def show(self):
        if ini.getProjectKey() is None:
            self.textBox.setText("")
        else:
            self.textBox.setText(ini.getProjectKey())
        CStatusBarDialog.show(self)

    ###########################################################################
    def close(self):
        CStatusBarDialog.close(self)
        self.textBox.clear()

    ###########################################################################
    def cancelClicked(self):
        self.close()

    ###########################################################################
    def okClicked(self):

        projectKey = ""
        if self.textBox.text() is not None:
            projectKey = str(self.textBox.text())

        ini.setProjectKey(projectKey)
        ini.save()

        logger.success("Project key modified successfully")

        self.close()


###########################################################################################
###########################################################################################
###########################################################################################

projectDialog = ProjectDialog()
