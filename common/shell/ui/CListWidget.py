from PyQtImports import QListWidget
from common.shell.ui.UI import WHITE, TRANSPARENT, mainComponentBorder


class CListWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)

        self.setStyleSheet(
            "QListWidget {" +
            "   background-color: " + WHITE + ";" +
            "   outline: 0;" +
            mainComponentBorder() +
            "}" +
            "QListWidget::item:selected {" +
            "   background-color: " + TRANSPARENT + ";" +
            "}" +
            "QListWidget::item:selected:hover {" +
            "   background-color: " + TRANSPARENT + ";" +
            "}" +
            "QListWidget::item:hover {" +
            "   background-color: " + TRANSPARENT + ";" +
            "}"
        )


"""
QListView {
    show-decoration-selected: 1; /* make the selection span the entire width of the view */
}

QListView::item:alternate {
    background: #EEEEEE;
}

QListView::item:selected {
    border: 1px solid #6a6ea9;
}

QListView::item:selected:!active {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #ABAFE5, stop: 1 #8588B2);
}

QListView::item:selected:active {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #6a6ea9, stop: 1 #888dd9);
}

QListView::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);
}
"""
