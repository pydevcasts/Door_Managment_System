import threading

from PyQtImports import QLabel
from common.shell.ui.dialog.CDialog import CDialog


class RequestExecuteThread(threading.Thread):
    def __init__(self, request, dialog):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.request = request
        self.dialog = dialog

    def run(self):
        from Globals import interface
        self.dialog.response = interface.get().handle(self.request)
        self.dialog.close()


class RequestWaitDialog(CDialog):

    def __init__(self, request):
        CDialog.__init__(self)

        label = QLabel("Please Wait ... ")
        self.addSingle(label)

        self.response = None

        RequestExecuteThread(request, self).start()

        self.show()
