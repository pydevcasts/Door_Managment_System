from PyQtImports import Qt, QPixmap, QCursor, QWidget, QGridLayout, QLabel
from common.shell.ui.CRowPanel import CRowPanel
from common.shell.ui.Constants import Constants
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import blackForeground, grayBackground


class SettingsPackWrapper:

    ################################################################################
    def __init__(self, wrapperFactory, settingsPack, parentWrapper=None, **kwargs):
        self.wrapperFactory = wrapperFactory
        self.settingsPack = settingsPack
        self.kwargs = kwargs
        self.parentWrapper = parentWrapper
        self.container = None
        self.widget = None
        self.rowPanel = None
        self.wrapperList = []

    ################################################################################
    def createUI(self):
        self.widget = self.createWidget()
        self.rowPanel = CRowPanel()
        self.createTitle()

        for setting in self.settingsPack.settingList:
            wrapper = self.wrapperFactory.wrap(setting, self, **self.kwargs)
            if wrapper is None:
                continue
            if isinstance(wrapper, SettingsPackWrapper):
                wrapper.activate()
            self.wrapperList.append(wrapper)
            wrapper.addTo(self.rowPanel)

        from Lang import lregister
        lregister(self)

    ################################################################################
    def __len__(self):
        return len(self.settingsPack)

    ################################################################################
    def addTo(self, rowPanel):
        rowPanel.addSingle(self.widget)

    ################################################################################
    def createWidget(self):
        widget = QWidget()
        widget.setMinimumSize(Constants.DEFAULT_EDITOR_HEIGHT, Constants.DEFAULT_EDITOR_HEIGHT)

        gridLayout = QGridLayout(widget)
        gridLayout.setContentsMargins(10, 5, 5, 5)
        gridLayout.setSpacing(10)
        gridLayout.setColumnStretch(1, 1)

        self.widgetText = QLabel(self.settingsPack.getTitle())
        # self.widgetText.setMinimumSize(Constants.DEFAULT_EDITOR_HEIGHT, Constants.DEFAULT_EDITOR_HEIGHT)
        self.widgetText.setStyleSheet(grayBackground())
        self.widgetText.setFont(Fonts.LabelFont)
        gridLayout.addWidget(self.widgetText, 0, 0)

        forwardLabel = QLabel()
        pixmap = QPixmap("images/forward32.png")
        forwardLabel.setPixmap(pixmap)
        forwardLabel.setStyleSheet(grayBackground())
        gridLayout.addWidget(forwardLabel, 0, 2)

        widget.setStyleSheet(grayBackground())
        widget.setCursor(QCursor(Qt.PointingHandCursor))
        widget.mousePressEvent = self.buttonClicked

        return widget

    ################################################################################
    def setTranslations(self):
        try:
            self.widgetText.setText(self.settingsPack.getTitle())
            self.titleText.setText(self.settingsPack.getTitle())
        except:
            pass

    ################################################################################
    def createTitle(self):
        if self.parentWrapper is None:
            return
        titlePanel = QWidget()
        titlePanel.setMinimumSize(Constants.DEFAULT_EDITOR_HEIGHT, Constants.DEFAULT_EDITOR_HEIGHT)

        gridLayout = QGridLayout(titlePanel)
        gridLayout.setContentsMargins(0, 0, 0, 10)
        gridLayout.setSpacing(10)
        gridLayout.setColumnStretch(2, 1)

        backLabel = QLabel()
        pixmap = QPixmap("images/back20.png")
        backLabel.setPixmap(pixmap)
        backLabel.setCursor(QCursor(Qt.PointingHandCursor))
        backLabel.mousePressEvent = self.backButtonClicked
        gridLayout.addWidget(backLabel, 0, 0)

        self.titleText = QLabel(self.settingsPack.getTitle())
        self.titleText.setStyleSheet(blackForeground())
        self.titleText.setFont(Fonts.TitleFont)
        gridLayout.addWidget(self.titleText, 0, 1)

        self.rowPanel.addSingle(titlePanel)

    ################################################################################
    def find(self, paramCode):
        for wrapper in self.wrapperList:
            try:
                result = wrapper.find(paramCode)
                if result is not None:
                    return result
            except:
                pass
        return None

    ################################################################################
    def findAll(self, paramCode):
        result = []
        for wrapper in self.wrapperList:
            try:
                wrappers = wrapper.findAll(paramCode)
                result.extend(wrappers)
                continue
            except:
                pass
            try:
                wrapper = wrapper.find(paramCode)
                if wrapper is not None:
                    result.append(wrapper)
            except:
                pass
        return result

    ################################################################################
    def getContainer(self):
        if self.container is not None:
            return self.container
        if self.parentWrapper is not None:
            return self.parentWrapper.getContainer()
        return None

    ################################################################################
    def buttonClicked(self, mouseEvent):
        self.activate()

    ################################################################################
    def backButtonClicked(self, mouseEvent):
        self.parentWrapper.activate()

    ################################################################################
    def activate(self, container=None):
        if self.widget is None:
            self.createUI()
        if container is not None:
            self.container = container
        container = self.getContainer()
        if container is None:
            return
        container.addWidget(self.rowPanel)
