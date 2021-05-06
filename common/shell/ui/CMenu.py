from PyQtImports import QMenu
from common.shell.ui.Fonts import Fonts
from common.shell.ui.UI import LIGHT_GRAY, GRAY, DARK_GRAY, BLACK


class CMenu(QMenu):

    def __init__(self, *__args):
        QMenu.__init__(self, *__args)

        self.setStyleSheet(
            "QMenu {" +
            "   Background-color: " + LIGHT_GRAY + "; " +
            "} " +
            "QMenu::item { " +
            "   color: " + BLACK + "; " +
            "   background-color: transparent; " +
            "   Padding: 8px 32px; " +
            "   Border-bottom:1px solid " + GRAY + "; " +
            str(Fonts.GroupFont) +
            "} " +
            "QMenu::item:selected { " +
            "   Background-color: " + DARK_GRAY + "; " +
            "}"
        )
