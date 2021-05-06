from Globals import logger
from PyQtImports import QGridLayout, QDialog, QLabel, QThread, QMovie


################################################################################
################################################################################
class WorkerThread(QThread):

    ############################################################################
    def __init__(self, runFunction, *argv, **argc):
        QThread.__init__(self)

        self.result = None

        self.runFunction = runFunction
        self.argv = argv
        self.argc = argc

    ############################################################################
    def run(self):
        try:
            self.result = self.runFunction(*self.argv, **self.argc)
        except Exception as e:
            self.result = e
            import traceback
            logger.exception(traceback.format_exc())


################################################################################
################################################################################
class WaitingDialog(QDialog):

    ############################################################################
    def __init__(self, text, handleFunction, runFunction, *argv, **argc):
        super(WaitingDialog, self).__init__(None)

        self.handleFunction = handleFunction

        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(0)
        gridLayout.setColumnStretch(1, 1)

        self.movie = QMovie("images/waiting.gif")
        image = QLabel()
        image.setMovie(self.movie)
        gridLayout.addWidget(image, 0, 0, 1, 1)

        label = QLabel(text)
        gridLayout.addWidget(label, 0, 1, 1, 1)

        self.thread = WorkerThread(runFunction, *argv, **argc)
        self.thread.finished.connect(self.close)

    ############################################################################
    def show(self):
        self.movie.start()
        self.thread.start()
        QDialog.exec_(self)

    ############################################################################
    def close(self):
        QDialog.close(self)
        self.movie.stop()

        if self.handleFunction is not None:
            self.handleFunction(self.thread.result)
