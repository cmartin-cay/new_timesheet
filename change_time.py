import sys

from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QComboBox,
    QApplication,
    QDoubleSpinBox,
    QLabel,
    QDialogButtonBox,
)

import current_time as ct
import populate_db


class ChangeTimeWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.combo_box = QComboBox(self)
        self.spinner = Spinner()
        self.client_text = QLabel("Client")
        self.time_text = QLabel("Time")

        self.combo_box.setEditable(True)
        self.combo_box.addItems(self.get_all_clients())
        self.combo_box.setCurrentIndex(-1)

        self.save_changes_button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.save_changes_button_box.accepted.connect(self.update_timesheet)
        self.save_changes_button_box.rejected.connect(self.close)

        grid_layout.addWidget(self.client_text, 0, 0, 1, 2)
        grid_layout.addWidget(self.time_text, 1, 0)
        grid_layout.addWidget(self.combo_box, 0, 1, 1, 2)
        grid_layout.addWidget(self.spinner, 1, 1)
        grid_layout.addWidget(self.save_changes_button_box, 2, 0, 1, 2)

    def update_timesheet(self):
        selected_client = self.combo_box.currentText()
        selected_value = self.spinner.value()
        ct.current_timesheet[selected_client] += selected_value

    def get_all_clients(self):
        active_set = set(populate_db.show_clients(active=True))
        timesheet_set = set(ct.current_timesheet.keys())
        active_set.update(timesheet_set)
        active_list = sorted(list(active_set), key=str.casefold)
        return active_list


class Spinner(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(1)
        self.setSingleStep(0.1)
        self.setMinimum(-100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ChangeTimeWidget()
    main_window.show()
    sys.exit(app.exec_())
