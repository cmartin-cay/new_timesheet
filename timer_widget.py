import json
import os
import sys
from collections import defaultdict
from datetime import datetime

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QApplication,
    QMessageBox,
)

import current_time as ct
import populate_db


class TimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)

        self.selected = ""
        self.start_time = None
        self.stop_time = None
        self.is_running = False

        self.create_combo_box()
        self.create_buttons()
        self.startup_logic()

        grid_layout.addWidget(self.combo_box, 0, 0, 1, 2)
        grid_layout.addWidget(self.start_button, 1, 0)
        grid_layout.addWidget(self.stop_button, 1, 1)

        self.status_label = QLabel()
        self.timer = QTimer()
        self.time_count = 0
        # Set a Timer to autosave the current_timesheet to json
        self.autosave_timer = QTimer()
        self.autosave_timer.start(1000 * 60 * 5)
        self.autosave_timer.timeout.connect(self.autosave)

    def create_combo_box(self):
        # TODO Insert policy for clients not in the default client list
        self.combo_box = QComboBox(self)
        self.combo_box.setMinimumWidth(200)
        self.combo_box.setEditable(True)
        self.combo_box.addItems(populate_db.show_clients(active=True))
        self.combo_box.setCurrentIndex(-1)
        self.combo_box.activated.connect(self.handle_activate)
        self.combo_box.currentTextChanged.connect(self.handle_activate)

    def create_buttons(self):
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(":enabled {background-color: green}")
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(":enabled {background-color: #FF0000}")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_timer)

    def startup_logic(self):
        try:
            with open("tmp_save.json", "r") as fp:
                data = json.load(fp)
                import_question = QMessageBox.question(
                    self, "Found timesheet", "Import existing timehseet?"
                )
                if import_question == QMessageBox.Yes:
                    ct.current_timesheet = defaultdict(float, data)
                else:
                    ct.current_timesheet = defaultdict(float)
                    self.delete_autosave()
        except FileNotFoundError:
            ct.current_timesheet = defaultdict(float)

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

    def stop_timer(self):
        self.stop_time = datetime.now()
        self.is_running = False
        ct.current_timesheet[self.selected] += self.elapsed_time(
            self.start_time, self.stop_time
        )
        self.combo_box.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # Reset Timer - For Slot/Signal purposes, a new QTimer needs to be created
        self.timer.stop()
        self.time_count = 0
        self.timer = QTimer()

    def elapsed_time(self, start, stop):
        return round((stop - start).seconds / 3600, 1)

    def save_time(self):
        if self.is_running:
            QMessageBox.information(
                self, "Timer Running", "Please stop your Timer before saving"
            )
        else:
            populate_db.enter_multiple_times(time_dictionary=ct.current_timesheet)
            ct.current_timesheet = defaultdict(float)

    def status_timer(self):
        self.time_count += 1
        self.status_label.setText(f"{self.selected} for {self.time_count} minutes")

    def autosave(self):
        with open("tmp_save.json", "w") as fp:
            if self.is_running:
                tmp_timesheet = ct.current_timesheet.copy()
                tmp_timesheet[self.selected] += self.elapsed_time(
                    self.start_time, datetime.now()
                )
                json.dump(tmp_timesheet, fp)
            else:
                json.dump(ct.current_timesheet, fp)

    def delete_autosave(self):
        """Delete the contents of the temp save file"""
        try:
            os.remove("tmp_save.json")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TimerWidget()
    main_window.show()
    sys.exit(app.exec_())
