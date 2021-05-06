from PyQtImports import QFont

"""
class Fonts:

    @staticmethod
    def createFont(family, size, bold, italic):
        try:
            return create_Font(family, size, bold, italic)
        except:
            pass

        try:
            return create_Font.__func__(family, size, bold, italic)
        except:
            pass

    def create_Font(family, size, bold, italic):
        font = QFont()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        font.setItalic(italic)
        return font

    #FAMILY_TIMES = "Times New Roman"

    #FAMILY_SHELL = "MS Shell Dlg 2"

    FAMILY_ARIAL = "Arial"

    TitleFont = create_Font(FAMILY_ARIAL, 22, True, False)

    ListItemFont = create_Font(FAMILY_ARIAL, 11, True, False)

    GroupTitleFont = create_Font(FAMILY_ARIAL, 13, False, False)

    StatusFont = create_Font(FAMILY_ARIAL, 10, True, False)

    StatusFontFocused = create_Font(FAMILY_ARIAL, 12, True, False)

    passwordsFont = create_Font(FAMILY_ARIAL, 10, True, False)

    LabelFont = create_Font(FAMILY_ARIAL, 11, False, False)

    CommandFont = create_Font(FAMILY_ARIAL, 10, True, False)

    DisplayFont = create_Font(FAMILY_ARIAL, 10, False, False)

    DialogEditorFont = create_Font(FAMILY_ARIAL, 9, False, False)

    DialogTextFont = create_Font(FAMILY_ARIAL, 9, False, False)

    DialogButtonFont = create_Font(FAMILY_ARIAL, 9, False, False)
"""


class CFont(QFont):
    def __init__(self, family, size, bold, italic):
        QFont.__init__(self)
        self.setFamily(family)
        self.setPointSize(size)
        self.setBold(bold)
        self.setItalic(italic)

    def __repr__(self):

        text = 'font-family: "' + self.family() + '"; font-size: ' + str(self.pointSize()) + 'pt;'
        if self.bold() or self.italic():
            text += ' font-style: '
        if self.bold():
            text += 'bold '
        if self.italic():
            text += 'italic '

        return text


class Fonts:

    def createFont(family, size, bold, italic):
        return CFont(family, size, bold, italic)

    # FAMILY_TIMES = "Times New Roman"

    # FAMILY_SHELL = "MS Shell Dlg 2"

    FAMILY_ARIAL = "Arial"

    TitleFont = createFont(FAMILY_ARIAL, 22, True, False)

    ListItemFont = createFont(FAMILY_ARIAL, 11, True, False)

    GroupTitleFont = createFont(FAMILY_ARIAL, 13, False, False)

    StatusFont = createFont(FAMILY_ARIAL, 10, True, False)

    StatusFontFocused = createFont(FAMILY_ARIAL, 12, True, False)

    passwordsFont = createFont(FAMILY_ARIAL, 10, True, False)

    LabelFont = createFont(FAMILY_ARIAL, 11, False, False)

    CommandFont = createFont(FAMILY_ARIAL, 10, True, False)

    DisplayFont = createFont(FAMILY_ARIAL, 10, False, False)

    DialogEditorFont = createFont(FAMILY_ARIAL, 9, False, False)

    DialogTextFont = createFont(FAMILY_ARIAL, 9, False, False)

    DialogButtonFont = createFont(FAMILY_ARIAL, 9, False, False)

    GroupFont = createFont(FAMILY_ARIAL, 10, True, False)
