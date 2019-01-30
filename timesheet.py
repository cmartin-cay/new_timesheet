import sys
from client_lists import ClientList

from PySide2.QtWidgets import (
    QMainWindow,
    QAction,
    QApplication,
    QStatusBar,
    QMessageBox,
    QFrame)

from timer_widget import TimerWidget


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
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(save_action)

        #Set up the Edit Menu
        edit_menu = menu_bar.addMenu("Edit")
        client_action = QAction("Clients", self)
        edit_menu.addAction(client_action)

        # Connect the buttons
        save_action.triggered.connect(self.timer_widget.save_time)
        close_action.triggered.connect(self.close)
        client_action.triggered.connect(self.show_client_list)

        # Set up the statusbar
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(self.timer_widget.status_label)
        self.setStatusBar(self.status_bar)

    def show_client_list(self):
        self.dialog = ClientList(parent=self)
        self.dialog.setModal(True)
        self.dialog.show()

    def closeEvent(self, event):
        if self.timer_widget.is_running:
            ret = self.close_menu_dialog("Your Timesheet is still running!")
            if ret == QMessageBox.No:
                event.ignore()
                return
        if self.timer_widget.current_timesheet:
            ret = self.close_menu_dialog("You have not saved your Timesheet!")
            if ret == QMessageBox.No:
                event.ignore()
                return
        self.timer_widget.delete_autosave()
        event.accept()

    def close_menu_dialog(self, set_text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Exit Warning")
        msg_box.setText(set_text)
        msg_box.setInformativeText("Are you sure you want to exit?")
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
