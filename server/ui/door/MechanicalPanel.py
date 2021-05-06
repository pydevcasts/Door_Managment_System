from Lang import lget, DOOR_IS_MECHANICAL
from PyQtImports import QWidget, QGridLayout, QLabel
from common.kernel.core.Role import *
from common.shell.ui.CLightButton import CLightButton
from common.shell.ui.Fonts import Fonts
from common.shell.ui.dialog.CQuestionDialog import CQuestionDialog


class MechanicalPanel(QWidget):

    #############################################################################
    def __init__(self, doorPanel, role):
        QWidget.__init__(self)
        self.doorPanel = doorPanel

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 3)

        row = 1

        label = QLabel(lget(DOOR_IS_MECHANICAL))
        label.setFont(Fonts.GroupTitleFont)
        layout.addWidget(label, row, 1, 1, 1)
        layout.setRowStretch(row + 1, 1)
        row += 2

        if role >= ROLE_ADVANCED_USER:
            sskButton = CLightButton("Enable SSK", "images/ssk.png", 68, self.doorPanel.onSskClicked)
            layout.addWidget(sskButton, row, 1, 1, 1)
            layout.setRowStretch(row + 1, 1)
            row += 2

        if role >= ROLE_OWNER:
            digitalButton = CLightButton("Enable DMS", "images/digital.png", 68, self.enableDigital)
            layout.addWidget(digitalButton, row, 1, 1, 1)
            layout.setRowStretch(row + 1, 1)
            row += 2

        layout.setRowStretch(row, 3)

    ##############################################################################
    def enableDigital(self):
        dialog = CQuestionDialog("Switch to digital state?")
        if not dialog.show():
            return

        from common.kernel.request.EnableMechanicalRequest import EnableMechanicalRequest
        request = EnableMechanicalRequest(False)
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

        self.doorPanel.alert("Digital state enabled successfully.")
