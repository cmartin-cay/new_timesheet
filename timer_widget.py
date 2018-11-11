import sys
from datetime import datetime

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QApplication,
)

import populate_db


class TimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)

        self.selected = None
        self.start_time = None
        self.stop_time = None
        self.is_running = False

        self.create_combo_box()
        self.create_buttons()

        grid_layout.addWidget(self.combo_box, 0, 0, 1, 2)
        grid_layout.addWidget(self.start_button, 1, 0)
        grid_layout.addWidget(self.stop_button, 1, 1)

        self.status_label = QLabel()
        self.timer = QTimer()
        self.time_count = 0

    def create_combo_box(self):
        self.combo_box = QComboBox(self)
        self.combo_box.setEditable(True)
        self.combo_box.addItems(populate_db.show_clients(active=True))
        self.combo_box.setCurrentIndex(-1)
        self.combo_box.activated.connect(self.handle_activate)
        self.combo_box.currentTextChanged.connect(self.handle_activate)

    def create_buttons(self):
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.end_timer)

    def handle_activate(self, index):
        self.selected = self.combo_box.currentText()

    def start_timer(self):
        self.start_time = datetime.now()
        self.is_running = True
        self.combo_box.setEnabled(False)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText(f"{self.selected} for {self.time_count} minutes")
        # Set the timer for 1 minute intervals
        self.timer.start(1000 * 60)
        self.timer.timeout.connect(self.status_timer)

    def end_timer(self):
        self.stop_time = datetime.now()
        self.is_running = False
        self.combo_box.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # Reset Timer - For Slot/Signal purposes, a new QTimer needs to be created
        self.timer.stop()
        self.time_count = 0
        self.timer = QTimer()

    def save_time(self):
        populate_db.enter_time(
            name=self.selected,
            total_time=round((self.stop_time - self.start_time).seconds / 3600, 1),
        )

    def status_timer(self):
        self.time_count += 1
        self.status_label.setText(f"{self.selected} for {self.time_count} minutes")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TimerWidget()
    main_window.show()
    sys.exit(app.exec_())
