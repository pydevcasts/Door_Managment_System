from PyQtImports import QWidget


########################################################################
########################################################################
class EditorA(QWidget):

    ################################################################
    def __init__(self, setting):

        QWidget.__init__(self)
        self.setting = setting
        self.valueChangeListeners = []

    ################################################################
    def addValueChangeListener(self, listener):
        if listener is None:
            return
        self.valueChangeListeners.append(listener)

    ################################################################
    def valueChanged(self):
        for listener in self.valueChangeListeners:
            listener.valueChanged(self)

    ################################################################
    def getValue(self):
        raise Exception("EditorA.getValue - Not Implemented")

    ################################################################
    def setValue(self, value):
        raise Exception("EditorA.setValue - Not Implemented")

    ################################################################
    def setTranslations(self):
        pass
