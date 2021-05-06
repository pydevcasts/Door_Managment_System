from Lang import lget, NOW, SECONDS_AGO, MINUTES_AGO, HOURS_AGO, HOURS_MINUTES_AGO
from PyQtImports import QWidget, QGridLayout, QLabel, QPixmap
from common.kernel.core.DoorErrors import doorErrors
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import whiteBackground, noBorder, mainComponentBorder, darkGrayForeground


class ErrorWidget(QWidget):

    #######################################################################################
    def __init__(self, error):

        QWidget.__init__(self)

        errorCode = error[0]

        self.innerPanel = QWidget()
        innerLayout = QGridLayout(self.innerPanel)
        innerLayout.setContentsMargins(10, 10, 10, 10)
        innerLayout.setSpacing(10)
        innerLayout.setColumnStretch(2, 1)

        self.image = QLabel(self.innerPanel)
        innerLayout.addWidget(self.image, 0, 0, 2, 1)
        pixmap = QPixmap(doorErrors.getImageAddress(errorCode))
        self.image.setPixmap(pixmap)

        self.textLabel = QLabel(self.innerPanel)
        self.textLabel.setStyleSheet(darkGrayForeground())
        self.textLabel.setFont(Fonts.StatusFont)
        self.textLabel.setText(lget(doorErrors.find(errorCode).message))
        innerLayout.addWidget(self.textLabel, 0, 1, 1, 1)

        self.timeLabel = QLabel(self.innerPanel)
        self.timeLabel.setStyleSheet(darkGrayForeground())
        self.timeLabel.setText(self.getTimeString(error[1]))
        innerLayout.addWidget(self.timeLabel, 1, 1, 1, 1)

        self.middlePanel = QWidget()
        middleLayout = QGridLayout(self.middlePanel)
        middleLayout.setContentsMargins(5, 5, 5, 5)
        middleLayout.setSpacing(0)
        middleLayout.setColumnStretch(1, 1)
        middleLayout.setRowStretch(0, 1)
        middleLayout.setRowStretch(2, 1)

        middleLayout.addWidget(self.innerPanel, 1, 0, 1, 1)

        outerlayout = QGridLayout(self)
        outerlayout.setContentsMargins(0, 0, 0, 0)
        outerlayout.setSpacing(0)

        outerlayout.addWidget(self.middlePanel, 0, 0, 1, 1)

        self.setStyleSheet(mainComponentBorder())
        self.middlePanel.setStyleSheet(whiteBackground())
        self.innerPanel.setStyleSheet(noBorder())

    #######################################################################################
    # def setTranslations(self):
    #    self.textLabel.setText(lget(self.baseStatus.text))

    #######################################################################################
    def getTimeString(self, millies):

        seconds = int(millies / 1000)

        if seconds <= 5:
            return lget(NOW)

        minutes = int(seconds / 60)
        seconds %= 60
        if minutes == 0:
            return lget(SECONDS_AGO, seconds)

        hours = int(minutes / 60)
        minutes %= 60
        if hours == 0:
            return lget(MINUTES_AGO, minutes)
        if minutes == 0:
            return lget(HOURS_AGO, hours)

        return lget(HOURS_MINUTES_AGO, hours, minutes)
