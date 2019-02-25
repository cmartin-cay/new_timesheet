import sys

from PySide2.QtWidgets import (
    QMainWindow,
    QAction,
    QApplication,
    QStatusBar,
    QMessageBox,
)

from client_lists import ClientList
from timer_widget import TimerWidget
from timesheet_viewer import CurrentTimesheetViewer
from timesheet_to_excel import Viewer
import current_time as ct
from collections import defaultdict


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setting a Central Widget
        self.timer_widget = TimerWidget(parent=self)
        self.setCentralWidget(self.timer_widget)
        self.setWindowTitle("Timesheet")

        # Set up a menubar
        menu_bar = self.menuBar()

        # Set up the File Menu
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        close_action = QAction("Close", self)
        save_action = QAction("Save", self)
        clear_action = QAction("Clear", self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(save_action)
        file_menu.addAction(clear_action)

        # Set up the Edit Menu
        edit_menu = menu_bar.addMenu("Edit")
        client_action = QAction("View Clients", self)
        viewer_action = QAction("Current Timesheet", self)
        export_action = QAction("Weekly Timesheet", self)
        edit_menu.addAction(client_action)
        edit_menu.addAction(viewer_action)
        edit_menu.addAction(export_action)

        # Connect the buttons
        save_action.triggered.connect(self.timer_widget.save_time)
        clear_action.triggered.connect(self.clear_timesheet)
        close_action.triggered.connect(self.close)
        client_action.triggered.connect(self.show_client_list)
        viewer_action.triggered.connect(self.show_current_timesheet)
        export_action.triggered.connect(self.show_viewer)

        # Set up the statusbar
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(self.timer_widget.status_label)
        self.setStatusBar(self.status_bar)

    def show_client_list(self):
        self.dialog = ClientList(parent=self)
        self.dialog.setModal(True)
        self.dialog.show()

    def clear_timesheet(self, event):
        if ct.current_timesheet:
            ret = self.close_menu_dialog(set_text="Clear Timesheet Entries!", set_info_text="This will delete all timesheet entries for today. Are you sure?")
            if ret == QMessageBox.No:
                return
            else:
                ct.current_timesheet = defaultdict(float)

    def show_current_timesheet(self):
        self.dialog = CurrentTimesheetViewer(parent=self)
        self.dialog.setModal(True)
        self.dialog.show()

    def show_viewer(self):
        self.dialog = Viewer(parent=self)
        self.dialog.setModal(True)
        self.dialog.show()

    def closeEvent(self, event):
        if self.timer_widget.is_running:
            ret = self.close_menu_dialog(set_text="Your Timesheet is still running!", set_info_text="Are you sure you want to exit?")
            if ret == QMessageBox.No:
                event.ignore()
                return
        if ct.current_timesheet:
            ret = self.close_menu_dialog(set_text="You have not saved your Timesheet!", set_info_text="Are you sure you want to exit?")
            if ret == QMessageBox.No:
                event.ignore()
                return
        self.timer_widget.delete_autosave()
        event.accept()

    def close_menu_dialog(self, set_text, set_info_text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Exit Warning")
        msg_box.setText(set_text)
        msg_box.setInformativeText(set_info_text)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        ret = msg_box.exec_()
        return ret


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
