from client.shell.admin.editor.CheckEditor import CheckEditor
from client.shell.admin.editor.ComboEditor import ComboEditor
from common.kernel.setting.ListSetting import ListSetting
from common.kernel.setting.ToggleSetting import ToggleSetting
from common.shell.editor.EditorFactory import EditorFactory as CommonEditorFactory


class EditorFactory(CommonEditorFactory):

    def __init__(self):
        CommonEditorFactory.__init__(self)

    def getEditor(self, setting):

        if isinstance(setting, ToggleSetting):
            return CheckEditor(setting)

        if isinstance(setting, ListSetting):
            return ComboEditor(setting)

        return CommonEditorFactory.getEditor(self, setting)


#####################################################
#####################################################
#####################################################
editorFactory = EditorFactory()
