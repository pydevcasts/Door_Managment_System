import threading

from Lang import lget, CANCEL, SCAN, OK, ERROR
from PyQtImports import QLabel, QMovie, pyqtSignal
from common.shell.ui.dialog.CDialog import CDialog


class InitialSetupDialog(CDialog):
    updateOkButtonSignal = pyqtSignal(bool, bool)
    updateTextSignal = pyqtSignal(str, str)
    updateAnimationSignal = pyqtSignal(str)

    ####################################################################################
    def __init__(self, onStart, onCancel, onScan):
        CDialog.__init__(self)

        self.onStart = onStart
        self.onCancel = onCancel
        self.onScan = onScan

        self.cancelButton = self.addButton(CANCEL)
        self.cancelButton.clicked.connect(self.cancel)

        self.scanButton = self.addButton(SCAN)
        self.scanButton.clicked.connect(self.scan)

        self.okButton = self.addButton(OK)
        self.okButton.setVisible(False)
        self.okButton.clicked.connect(self.ok)

        self.imageWidget = QLabel()
        self.addSingle(self.imageWidget)

        self.textWidget1 = QLabel()
        self.addSingle(self.textWidget1)
        self.textWidget2 = QLabel()
        self.addSingle(self.textWidget2)

        self.movie = None

        self.updateOkButtonSignal.connect(self.updateOkButtonSlot)
        self.updateTextSignal.connect(self.updateTextSlot)
        self.updateAnimationSignal.connect(self.updateAnimationSlot)

        self.updateText("Open the door completely by hand, then press the scan button.")
        self.updateAnimation("images/open_by_hand.gif")

        self.start()

    ####################################################################################
    def updateOkButton(self, visible, enabled=False):
        self.updateOkButtonSignal.emit(visible, enabled)

    ####################################################################################
    def updateOkButtonSlot(self, visible, enabled):
        self.scanButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.okButton.setVisible(visible)
        self.okButton.setEnabled(enabled)

    ####################################################################################
    def updateText(self, text1, text2=""):
        self.updateTextSignal.emit(text1, text2)

    ####################################################################################
    def updateTextSlot(self, text1, text2):
        self.textWidget1.setText(lget(text1))
        self.textWidget2.setText(lget(text2))

    ####################################################################################
    def updateAnimation(self, animationAddress):
        self.updateAnimationSignal.emit(animationAddress)

    ####################################################################################
    def pauseAnimation(self):
        self.updateAnimationSignal.emit("")

    ####################################################################################
    def updateAnimationSlot(self, animationAddress):
        if (animationAddress is None or len(animationAddress) == 0) and self.movie is not None:
            self.movie.setPaused(True)
            return

        if self.movie is not None:
            self.movie.stop()

        self.movie = QMovie(animationAddress)
        self.imageWidget.setMovie(self.movie)
        self.movie.start()

    ####################################################################################
    def start(self):
        threading.Thread(target=self.startThread).start()

    ####################################################################################
    def startThread(self):

        if not self.onStart():
            self.movie.stop()
            self.updateText(ERROR)
            self.updateOkButton(True, True)
            self.pauseAnimation()

    ####################################################################################
    def cancel(self, _):
        threading.Thread(target=self.cancelThread).start()

    ####################################################################################
    def cancelThread(self):
        self.updateOkButton(True)
        self.updateText("Scanning canceled.")
        self.pauseAnimation()
        self.onCancel()
        self.updateOkButton(True, True)

    ####################################################################################
    def scan(self, _):
        threading.Thread(target=self.scanThread).start()

    ####################################################################################
    def scanThread(self):
        # set text to scanning
        self.updateOkButton(True)
        self.updateText("Scanning the door, please wait...")
        self.updateAnimation("images/scanning.gif")

        success = self.onScan()

        self.pauseAnimation()

        if success:
            self.updateText("Scanning finished successfully.")
        else:
            self.updateText("Scanning finished with errors.")

        self.updateOkButton(True, True)

    ####################################################################################
    def ok(self, _):
        self.close()
