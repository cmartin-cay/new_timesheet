import sys
from datetime import datetime
from client_lists import ClientList

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import (
    QMainWindow,
    QComboBox,
    QPushButton,
    QWidget,
    QGridLayout,
    QAction,
    QApplication,
    QStatusBar,
    QLabel,
)

import populate_db


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setting a Central Widget
        self.email_blast_widget = EmailBlast(parent=self)
        self.setCentralWidget(self.email_blast_widget)
        self.setWindowTitle("Timesheet")
        self.client_list = ClientList()
        # Set up a menubar and File menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        close_action = QAction("Close", self)
        save_action = QAction("Save", self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(save_action)
        # Connect the buttons
        save_action.triggered.connect(self.email_blast_widget.enter_time)
        open_action.triggered.connect(self.client_list.show)

        # Set up a statusbar
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(self.email_blast_widget.status_label)
        self.setStatusBar(self.status_bar)


class EmailBlast(QWidget):
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
        self.timer.start(1000)
        self.timer.timeout.connect(self.status_timer)

    def end_timer(self):
        self.stop_time = datetime.now()
        self.is_running = False
        self.combo_box.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # Reset Timer - for reasons I don't understand a new QTimer needs to be created
        self.timer.stop()
        self.time_count = 0
        self.timer = QTimer()

    def enter_time(self):
        populate_db.enter_time(
            name=self.selected, start=self.start_time, end=self.stop_time
        )

    def status_timer(self):
        self.time_count += 1
        self.status_label.setText(f"{self.selected} for {self.time_count} minutes")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
