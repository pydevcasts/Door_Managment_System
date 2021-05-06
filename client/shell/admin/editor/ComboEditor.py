from PyQtImports import QGridLayout, QComboBox
from PyQtImports import Qt
from common.shell.editor.EditorA import EditorA


##########################################################################
##########################################################################
class CustomComboBox(QComboBox):

    def __init__(self):
        QComboBox.__init__(self)
        self.setMinimumSize(25, 25)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if not self.hasFocus():
            event.ignore()
        else:
            QComboBox.wheelEvent(event)


##########################################################################
##########################################################################
class ComboEditor(EditorA):

    def __init__(self, setting):
        EditorA.__init__(self, setting)

        self.layout = QGridLayout(self)
        self.layout.setColumnStretch(0, 1)

        self.combobox = CustomComboBox()

        self.items = setting.getDataList()
        for item in self.items:
            self.combobox.addItem(str(item), item)

        self.combobox.currentIndexChanged.connect(self.indexChanged)
        self.layout.addWidget(self.combobox, 0, 0, 1, 1)

    ########################################################################
    def indexChanged(self):
        self.valueChanged()

    ########################################################################
    def getValue(self):  # getEditorValue
        return self.combobox.itemData(self.combobox.currentIndex()).key

    ########################################################################
    def setValue(self, value):
        item = self.items.find(value)
        index = self.combobox.findText(str(item))
        if index >= 0:
            self.combobox.setCurrentIndex(index)
