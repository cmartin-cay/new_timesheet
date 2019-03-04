import sys

from PySide2.QtWidgets import QWidget, QGridLayout, QComboBox, QApplication

import current_time as ct
import populate_db


class ChangeTimeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.combo_box = QComboBox(self)
        self.combo_box.setEditable(True)
        self.combo_box.activated.connect(self.handle_activate)
        self.combo_box.currentTextChanged.connect(self.handle_activate)
        self.combo_box.addItems(self.get_all_clients())

        grid_layout.addWidget(self.combo_box, 0, 0, 1, 2)

    def handle_activate(self, index):
        self.selected_client = self.combo_box.currentText()

    def get_all_clients(self):
        active_set = set(populate_db.show_clients(active=True))
        timesheet_set = set(ct.current_timesheet.keys())
        active_set.update(timesheet_set)
        active_list = sorted(list(active_set), key=str.casefold)
        return active_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ChangeTimeWidget()
    main_window.show()
    sys.exit(app.exec_())
