from PyQtImports import QLabel
from common.shell.ui.dialog.CDialog import CDialog


class CStatusBarDialog(CDialog):

    ############################################################################
    def __init__(self):
        CDialog.__init__(self)

        self.statusBar = QLabel()
        self.statusBar.setStyleSheet("color: rgb(255, 0, 0); ")# border:1px solid rgb(200, 200, 200);
        self.middleLayout.addWidget(self.statusBar, 0, 0, 1, 1)

    ############################################################################
    def setStatusText(self, textKey, *params):
        from Lang import lget
        text = lget(textKey, *params)
        from threading import Thread
        t = Thread(target=self.statusBar.setText, args=(text,))
        t.start()

    ############################################################################
    def statusListenTo(self, textBox):
        textBox.textEdited['QString'].connect(self.statusBar.clear)

    ############################################################################
    def close(self, accepted=None):
        CDialog.close(self, accepted)
        self.statusBar.clear()
