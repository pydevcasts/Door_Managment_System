from PyQtImports import QObject, QMetaObject, pyqtSignal
from client.kernel.setting.CommandImplFactory import commandImplFactory
from common.shell.ui.CPushButton import CPushButton
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog


class CommandWrapper(QObject):
    updateLabelTextSignal = pyqtSignal(object)

    ################################################################################
    def __init__(self, command):
        QObject.__init__(self)

        self.command = command
        self.commandImpl = commandImplFactory.getCommandImpl(command.getParameterCode())

        self.button = CPushButton(command.getTitle(), command.getImageAddress(), 32, self.clicked)

        QMetaObject.connectSlotsByName(self)
        self.updateLabelTextSignal.connect(self.setLabelText)

        from Lang import lregister
        lregister(self)

    ################################################################################
    def setTranslations(self):
        self.button.setText(self.commandImpl.getTitle())

    ################################################################################
    def addTo(self, rowPanel):
        rowPanel.addCenter(self.button)

    ################################################################################
    def clicked(self):
        self.createDialog()
        self.dialog.show()

    ################################################################################
    def getTitle(self):
        return self.command.getTitle()

    ################################################################################
    def getQuestion(self):
        return self.getTitle() + " will be started. Are you sure?"

    ################################################################################
    def getWaitingMessage(self):
        return "Please wait..."

    ################################################################################
    def getSuccessMessage(self):
        return self.getTitle() + " is done successfully."

    ################################################################################
    def getFailureMessage(self):
        return self.getTitle() + " failed."

    ################################################################################
    def createDialog(self):
        question = self.getQuestion() + "                             "
        self.dialog = CQuestionDialog(question, onOkClicked=self.okClicked)

    ################################################################################
    def okClicked(self):

        self.updateLabelTextSignal.emit(self.getWaitingMessage())

        request = self.createRequest()

        from Globals import interface
        response = interface.get().handle(request)

        if response.isSuccessful():
            self.updateLabelTextSignal.emit(self.getSuccessMessage())
        else:
            self.updateLabelTextSignal.emit(self.getFailureMessage())

        self.dialog.removeAllButtons()
        closeButton = self.dialog.addButton("Close")
        closeButton.clicked.connect(self.dialog.close)

        # self.label = None
        # self.dialog = None

    ################################################################################
    def createRequest(self):
        from common.kernel.request.CommandRequest import CommandRequest
        request = CommandRequest(self.commandImpl.getParameterCode())

        from client.shell.pc.PasswordManager import passwordManager
        passwordManager.fillRequest(request)

        return request

    ################################################################################
    def setLabelText(self, text):
        self.dialog.label.setText(text)
