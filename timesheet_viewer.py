import sys

from PySide2.QtWidgets import QApplication, QDialog, QGridLayout, QDialogButtonBox

from client_lists import ClientListWidget


class CurrentTimesheetViewer(QDialog):
    #TODO make this into a viwer with 2 columns, one for names and one for times (this will need QTableView)
    def __init__(self, parent=None, timer_widget=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.current_viewer = ClientListWidget()
        for key, val in timer_widget.current_timesheet.items():
            entry = f'{key}{":":<5}   {val:>5}'
            self.current_viewer.addItem(entry)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.close)
        grid_layout.addWidget(self.current_viewer)
        grid_layout.addWidget(self.button_box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CurrentTimesheetViewer()
    main_window.show()
    sys.exit(app.exec_())


