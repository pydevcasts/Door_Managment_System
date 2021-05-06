from PyQtImports import QGridLayout, QRadioButton
from common.shell.editor.EditorA import EditorA


##########################################################
##########################################################
class EditorRadioButton(QRadioButton):

    def __init__(self, item):
        QRadioButton.__init__(self, str(item))
        self.item = item
        self.value = item.key

    def setTranslations(self):
        self.setText(str(self.item))


##########################################################
##########################################################
class ListEditor(EditorA):

    ######################################################
    def __init__(self, setting):
        EditorA.__init__(self, setting)

        self.layout = QGridLayout(self)
        self.layout.setRowStretch(0, 1)

        self.radioButtons = []
        self.value = None

        row = 1
        for item in setting.getDataList():
            radio = EditorRadioButton(item)
            self.radioButtons.append(radio)
            if row == 1:
                self.value = radio.value
                radio.setChecked(True)
            radio.toggled.connect(lambda: self.radioButtonChanged(radio))
            self.layout.addWidget(radio, row, 0, 1, 1)
            row += 1

        self.layout.setRowStretch(row, 1)

    ######################################################
    def radioButtonChanged(self, currentRadioButton):
        for radioButton in self.radioButtons:
            if radioButton.isChecked():
                self.value = radioButton.value
        self.valueChanged()

    ######################################################
    def getValue(self):  # getEditorValue
        return self.value

    ######################################################
    def setValue(self, value):
        for radio in self.radioButtons:
            if radio.value == value:
                radio.setChecked(True)
                return

    ################################################################
    def setTranslations(self):
        for radio in self.radioButtons:
            radio.setTranslations()
