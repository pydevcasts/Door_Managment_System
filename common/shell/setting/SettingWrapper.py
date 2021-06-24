from Globals import logger
from Lang import lregister
from PyQtImports import QIcon, QCursor
from PyQtImports import QWidget, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQtImports import Qt, QObject, QMetaObject, QSize, pyqtSignal
from common.shell.editor.EditorFactory import editorFactory
from common.shell.setting.SettingInputDialog import SettingInputDialog
from common.shell.ui.Constants import Constants
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import transparentBackground, whiteBackground, darkGrayForeground, littleComponentBorder, \
    noBorder


class SettingWrapper(QObject):
    updateUISignal = pyqtSignal()

    def __init__(self, setting):
        QObject.__init__(self)

        self.setting = setting

        try:
            self.label = self.createLabel()
            self.text, self.editButton, self.display = self.createDisplay()
            self.editor = editorFactory.getEditor(setting)
            self.inputDialog = SettingInputDialog(self)
            """ SettingInputDialog=>The base class of the class hierarchy.

                When called, it accepts no arguments and returns a new featureless instance 
                that has no instance attributes and cannot be given any.
            """
        except Exception as e:
            import traceback
            logger.exception(traceback.format_exc())

        lregister(self)

        QMetaObject.connectSlotsByName(self)
        self.updateUISignal.connect(self.updateUI)
        self.setValue(setting.getValue())

    ################################################################################
    def addTo(self, rowPanel):
        rowPanel.addDouble(self.label, self.display)

    ################################################################################
    def getTitle(self):
        return self.setting.getTitle()

    ################################################################################
    def createLabel(self):
        label = QLabel()

        label.setMinimumSize(1, Constants.DEFAULT_EDITOR_HEIGHT)
        label.setMaximumSize(Constants.INFINITY_SIZE, Constants.DEFAULT_EDITOR_HEIGHT)

        label.setFont(Fonts.LabelFont)
        label.setText(self.getLabelText())
        label.setStyleSheet(darkGrayForeground())

        return label

    ################################################################################
    def getLabelText(self):
        return self.setting.getTitle() + ": "

    ################################################################################
    def createText(self):
        text = QLineEdit()

        text.setMinimumSize(1, Constants.DEFAULT_EDITOR_HEIGHT)
        text.setMaximumSize(Constants.INFINITY_SIZE, Constants.DEFAULT_EDITOR_HEIGHT)

        text.setFont(Fonts.DisplayFont)

        text.setReadOnly(True)
        return text

    ################################################################################
    def createEditButton(self):
        button = QPushButton()
        # button.setMinimumSize(Constants.DEFAULT_EDITOR_HEIGHT, Constants.DEFAULT_EDITOR_HEIGHT)
        # button.setMaximumSize(Constants.DEFAULT_EDITOR_HEIGHT, Constants.DEFAULT_EDITOR_HEIGHT)
        button.setFixedSize(24, 24)
        # button.setText("...")
        button.setIcon(QIcon('images/edit.png'))
        button.setIconSize(QSize(16, 16))
        button.setStyleSheet("border: none; outline: 0;")
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.clicked.connect(self.editButtonClicked)
        return button

    ################################################################################
    def createDisplay(self):
        text = self.createText()
        button = self.createEditButton()

        innerPanel = QWidget()
        innerPanel.setStyleSheet(noBorder())
        innerLayout = QGridLayout(innerPanel)
        innerLayout.setContentsMargins(5, 0, 5, 0)
        innerLayout.setSpacing(0)
        innerLayout.setColumnStretch(0, 1)

        innerLayout.addWidget(text, 0, 0, 1, 1)
        innerLayout.addWidget(button, 0, 1, 1, 1)

        middlePanel = QWidget()
        middleLayout = QGridLayout(middlePanel)
        middleLayout.setContentsMargins(0, 0, 0, 0)
        middleLayout.setSpacing(0)
        middleLayout.setColumnStretch(0, 1)
        # middleLayout.setColumnStretch(2, 1)
        # middleLayout.setRowStretch(0, 1)
        # middleLayout.setRowStretch(2, 1)

        middleLayout.addWidget(innerPanel, 0, 0, 1, 1)

        display = QWidget()
        displayLayout = QGridLayout(display)
        displayLayout.setContentsMargins(0, 0, 0, 0)
        displayLayout.setSpacing(0)

        displayLayout.addWidget(middlePanel, 0, 0, 1, 1)

        innerPanel.setStyleSheet(transparentBackground() + noBorder())
        display.setStyleSheet(whiteBackground() + littleComponentBorder())

        return text, button, display

    ################################################################################
    def setTranslations(self):
        self.label.setText(self.getLabelText())
        self.inputDialog.setTranslations()
        self.updateUISignal.emit()

    ################################################################################
    def editButtonClicked(self):
        try:
            self.editor.setValue(self.value)
            self.inputDialog.show()
        except Exception as e:
            import traceback
            logger.exception(traceback.format_exc())

    ################################################################################
    def getEditorValue(self):
        return self.editor.getValue()

    ################################################################################
    def inputDialogAccepted(self):
        value = self.getEditorValue()
        self.onNewValueAccepted(value)

    ################################################################################
    def setValue(self, value):
        self.value = value
        self.updateUISignal.emit()

    ################################################################################
    def updateUI(self):
        self.text.setText(self.setting.getTextForValue(self.value))

    ################################################################################
    def find(self, paramCode):
        if paramCode is not None and str(self.setting.getParameterCode()) == str(paramCode):
            return self
        return None

    ################################################################################
    def onNewValueAccepted(self, value):
        raise Exception("Not implemented")
