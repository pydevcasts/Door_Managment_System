from PyQtImports import QPixmap, QMovie
from PyQtImports import QSplashScreen
from PyQtImports import Qt, pyqtSlot


class CSplash(QSplashScreen):

    def __init__(self):
        # run event dispatching in another thread
        QSplashScreen.__init__(self, QPixmap(), Qt.WindowStaysOnTopHint)
        self.movie = QMovie('images/splash.gif')
        #self.connect(self.movie, SIGNAL('frameChanged(int)'), SLOT('onNextFrame()'))
        self.movie.frameChanged['int'].connect(self.onNextFrame)
        self.movie.start()

    @pyqtSlot()
    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())


########################################################################################################################
########################################################################################################################
########################################################################################################################
splash = CSplash()
