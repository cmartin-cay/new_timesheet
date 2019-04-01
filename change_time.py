import sys

from PySide2.QtWidgets import (
    QDialog,
    QFormLayout,
    QVBoxLayout,
    QComboBox,
    QApplication,
    QDoubleSpinBox,
    QDialogButtonBox,
)

import current_time as ct
import populate_db


class ChangeTimeWidget(QDialog):
    def __init__(self, parent=None):
        #TODO Convert to a form layout
        super().__init__(parent)
        self.setWindowTitle("Change Time")
        self.setMinimumWidth(210)
        self.combo_box = QComboBox()

        self.spinner = Spinner()
        self.combo_box.setEditable(True)
        self.combo_box.addItems(self.get_all_clients())
        self.combo_box.setCurrentIndex(-1)

        self.save_changes_button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.save_changes_button_box.accepted.connect(self.update_timesheet)
        self.save_changes_button_box.rejected.connect(self.close)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.addRow("Client:", self.combo_box)
        form_layout.addRow("Time:", self.spinner)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.save_changes_button_box)
        self.setLayout(main_layout)

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
