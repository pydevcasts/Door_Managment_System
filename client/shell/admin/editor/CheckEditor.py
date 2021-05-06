from PyQtImports import QGridLayout, QCheckBox
from common.shell.editor.EditorA import EditorA

###############################################################
###############################################################
class CheckEditor(EditorA):

    def __init__(self, setting):
        EditorA.__init__(self, setting)

        self.layout = QGridLayout(self)

        self.checkBox = QCheckBox()

        self.checkBox.stateChanged.connect(self.stateChanged)
        self.layout.addWidget(self.checkBox, 0, 0, 1, 1)

    ##########################################################
    def stateChanged(self, int):
        self.valueChanged()

    ##########################################################
    def getValue(self): #getEditorValue
        if self.checkBox.isChecked():
            return 1
        return 0

    ##########################################################
    def setValue(self, value):
        self.checkBox.setChecked(value == 1)
