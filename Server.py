#!/usr/bin/env python
import sys
import traceback
from PyQtImports import QApplication
from Globals import logger


def main():
    app = QApplication(sys.argv)

    from server.core.Ini import Ini
    from Globals import ini
    ini.wrap(Ini())

    try:
        # create and show main window
        from server.ui.MainWindow import mainWindow
        mainWindow.show()

    except:
        logger.exception(traceback.format_exc())

    sys.exit(app.exec_())


if __name__ == "__main__":
    import ExceptHook
    main()
