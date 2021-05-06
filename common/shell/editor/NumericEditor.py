from PyQtImports import Qt, QGridLayout, QLabel, QSlider
from common.shell.editor.EditorA import EditorA


########################################################################
########################################################################
class CustomSlider(QSlider):
    ################################################################
    def __init__(self, orientation):
        QSlider.__init__(self, orientation)
        self.setFocusPolicy(Qt.StrongFocus)

    ################################################################
    def wheelEvent(self, event):
        if not self.hasFocus():
            event.ignore()
        else:
            QSlider.wheelEvent(event)


########################################################################
########################################################################
class NumericEditor(EditorA):

    ################################################################
    def __init__(self, setting):
        EditorA.__init__(self, setting)

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setColumnStretch(0, 1)

        self.slider = CustomSlider(Qt.Horizontal)
        self.slider.setMinimum(self.setting.minValue)
        self.slider.setMaximum(self.setting.maxValue)

        from common.shell.ui.UI import ORANGE
        self.slider.setStyleSheet("QSlider::handle:horizontal {background: " + ORANGE + ";}")

        self.slider.setMinimumSize(300, 20)

        self.slider.setTickInterval(5)
        self.slider.setTickPosition(QSlider.TicksBelow)

        from common.shell.ui.Fonts import Fonts
        self.slider.setFont(Fonts.DialogEditorFont)

        layout.addWidget(self.slider, 0, 0, 1, 1)

        self.valueLabel = QLabel(self.setting.getTextForValue(self.getValue()))
        self.valueLabel.setMaximumSize(70, 20)
        self.valueLabel.setMinimumSize(70, 20)
        layout.addWidget(self.valueLabel, 0, 1, 1, 1)

        self.slider.valueChanged.connect(self.sliderValueChange)

    ################################################################
    def sliderValueChange(self):
        self.valueLabel.setText(self.setting.getTextForValue(self.getValue()))
        self.valueChanged()

    ################################################################
    def getValue(self):  # getEditorValue
        return self.slider.value()

    ################################################################
    def setValue(self, value):  # updateEditor
        self.slider.setValue(value)

    ################################################################
    def setTranslations(self):
        self.valueLabel.setText(self.setting.getTextForValue(self.getValue()))
