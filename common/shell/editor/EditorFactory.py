from common.kernel.setting.ListSetting import ListSetting
from common.kernel.setting.NumericSetting import NumericSetting
from common.shell.editor.ListEditor import ListEditor
from common.shell.editor.NumericEditor import NumericEditor


class EditorFactory:

    def __init__(self):
        pass

    def getEditor(self, setting):

        if isinstance(setting, ListSetting):
            return ListEditor(setting)

        if isinstance(setting, NumericSetting):
            return NumericEditor(setting)

        return None

#####################################################
#####################################################
#####################################################
editorFactory = EditorFactory()
