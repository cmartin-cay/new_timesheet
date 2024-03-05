import sys

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QDialogButtonBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)

import current_time as ct
from client_lists import ClientListWidget


class CurrentTimesheetViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Current Timesheet")
        grid_layout = QGridLayout(self)
        rows = len(ct.current_timesheet)
        entries = list(ct.current_timesheet.items())
        self.current_viewer = QTableWidget()
        self.current_viewer.setRowCount(rows)
        self.current_viewer.setColumnCount(2)
        self.current_viewer.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.current_viewer.setSelectionMode(QAbstractItemView.NoSelection)
        self.current_viewer.setHorizontalHeaderLabels(["Client", "Time"])
        for i in range(0, rows):
            client, time = entries[i]
            client = QTableWidgetItem(client)
            time = QTableWidgetItem(str(time))
            self.current_viewer.setItem(i, 0, client)
            self.current_viewer.setItem(i, 1, time)
        self.current_viewer.resizeColumnsToContents()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.close)
        grid_layout.addWidget(self.current_viewer)
        grid_layout.addWidget(self.button_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CurrentTimesheetViewer()
    main_window.show()
    sys.exit(app.exec())
