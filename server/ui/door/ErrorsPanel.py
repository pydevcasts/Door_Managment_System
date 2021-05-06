from PyQtImports import QWidget, QGridLayout, QHBoxLayout, QFrame, QScrollArea, QPushButton, QIcon, QSize, QCursor, Qt, \
    QFileDialog
from common.kernel.request.RecentErrorsRequest import RecentErrorsRequest
from common.shell.ui.CRowPanel import CRowPanel
from server.connection.ConnectionManager import connectionManager
from server.ui.door.ErrorWidget import ErrorWidget


class ErrorsPanel(QWidget):

    ############################################################################
    def __init__(self, doorPanel, role):
        QWidget.__init__(self)
        self.doorPanel = doorPanel

        outerLayout = QGridLayout(self)
        outerLayout.setContentsMargins(2, 2, 2, 2)
        outerLayout.setSpacing(5)
        outerLayout.setRowStretch(1, 1)
        outerLayout.setColumnStretch(1, 1)

        self.rowPanel = CRowPanel()
        scroll = QScrollArea()
        scroll.setWidget(self.rowPanel)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outerLayout.addWidget(scroll, 1, 0, 1, 2)

        buttonsWidget = QWidget()
        buttonsLayout = QHBoxLayout(buttonsWidget)
        outerLayout.addWidget(buttonsWidget, 0, 0, 1, 1)

        self.refreshButton = QPushButton()
        self.refreshButton.setIcon(QIcon("images/refresh.png"))
        self.refreshButton.setIconSize(QSize(24, 24))
        self.refreshButton.clicked.connect(self.refresh)
        self.refreshButton.setStyleSheet("border: none; outline: 0;")
        self.refreshButton.setCursor(QCursor(Qt.PointingHandCursor))
        buttonsLayout.addWidget(self.refreshButton)

        from common.kernel.core.Role import ROLE_OWNER
        if role >= ROLE_OWNER and connectionManager.get().getConnectionType() == connectionManager.CONNECTION_TYPE_WEB:
            self.downloadButton = QPushButton()
            self.downloadButton.setIcon(QIcon("images/download.png"))
            self.downloadButton.setIconSize(QSize(24, 24))
            self.downloadButton.clicked.connect(self.download)
            self.downloadButton.setStyleSheet("border: none; outline: 0;")
            self.downloadButton.setCursor(QCursor(Qt.PointingHandCursor))
            buttonsLayout.addWidget(self.downloadButton)

    ############################################################################
    def updateOn(self, doorI):
        pass

    ############################################################################
    def refresh(self):
        self.rowPanel.clear()

        request = RecentErrorsRequest()
        response, exception = self.doorPanel.callRequest(request)

        if exception is not None:
            self.doorPanel.error(exception)
            return

        if response is None or not response.isSuccessful():
            self.doorPanel.error()
            return

        errors = response.doorErrors
        if isinstance(errors, str):
            import json
            errors = json.loads(errors)

        for error in errors:
            self.rowPanel.addSingle(ErrorWidget(error))

    ############################################################################
    def download(self):
        if connectionManager.get().getConnectionType() != connectionManager.CONNECTION_TYPE_WEB:
            self.doorPanel.error("File download is available only in web connection.")

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        # the name filters must be a list
        file_dialog.setNameFilters(["Comma Separated Value Files (*.csv)"])
        file_dialog.selectNameFilter("Comma Separated Value Files (*.csv)")

        import os
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        file_dialog.setDirectory(desktop)

        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H-%M")
        file_dialog.selectFile("DMS-Log(" + dt_string + ")")

        # show the dialog
        if file_dialog.exec_():
            fileName = file_dialog.selectedFiles()[0]
            connectionManager.get().downloadLogFile(fileName)
