from Lang import lget, START_COMMAND
from common.shell.ui.CPushButton import CPushButton
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog


class CommandWrapper(CPushButton):

    ################################################################################
    def __init__(self, command, doorPanel):
        self.command = command
        self.doorPanel = doorPanel
        CPushButton.__init__(self, command.getTitle(), command.getImageAddress(), 32, self.onClicked)
        """ this is attr without refrenses"""
        from Lang import lregister
        lregister(self)

    ################################################################################
    def setTranslations(self):
        """ this is for language argu of language inside of pyqt """
        self.setText(lget(self.command.getTitle()))

    ################################################################################
    def addTo(self, rowPanel):
        rowPanel.addCenter(self)

    ################################################################################
    def onClicked(self):
        dialog = CQuestionDialog(lget(START_COMMAND, self.command.getTitle()))
        dialog.show()
        if not dialog.isAccepted():
            return

        self.execute()

    ############################################################################
    def execute(self):

        from common.kernel.request.CommandRequest import CommandRequest
        request = CommandRequest(self.command.getParameterCode())
        response, exception = self.doorPanel.callRequest(request)
        """ this is attr without refrenses"""
        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        if response.isBuffered():
            # TODO a waiting mechanism
            self.doorPanel.alert("It might take a few seconds")
            return

        self.doorPanel.alert('"' + self.command.getTitle() + '" executed successfully')
