from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.CStatusButton import CStatusButton
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog


class StatusPanel(CRowPanel):

    #######################################################################################
    def __init__(self, doorPanel):
        CRowPanel.__init__(self)
        self.doorPanel = doorPanel

        baseStatusList = doorPanel.struct.getDoorStatusList()
        self.statusButtons = []
        for baseStatus in baseStatusList:
            button = CStatusButton(baseStatus, self.statusButtonClicked)
            self.statusButtons.append(button)
            self.addSingle(button)

        self.statusChanged(-1)

    #######################################################################################
    def statusButtonClicked(self, baseStatus):
        dialog = CQuestionDialog("Change status to " + str(baseStatus) + "?")
        if not dialog.show():
            return

        from common.kernel.request.SetStatusRequest import SetStatusRequest
        request = SetStatusRequest(baseStatus.key)
        response, exception = self.doorPanel.callRequest(request)

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

        # Status might be displayed in other door list listeners, so let's ask it to change the value and notify others
        from server.core.DoorList import doorList
        doorList.changeStatus(self.doorPanel.getDoor().serial, baseStatus.key)

    #######################################################################################
    def updateOn(self, doorI):
        self.statusChanged(doorI.status)

    #######################################################################################
    def statusChanged(self, status):
        for button in self.statusButtons:
            if button.baseStatus.key == status:
                button.select()
            else:
                button.unselect()
