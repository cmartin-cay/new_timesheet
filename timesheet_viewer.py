import sys

from PySide2.QtWidgets import QApplication, QDialog, QGridLayout, QDialogButtonBox

from client_lists import ClientListWidget


class CurrentTimesheetViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)

        self.current_viewer = ClientListWidget()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.close)
        grid_layout.addWidget(self.current_viewer)
        grid_layout.addWidget(self.button_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CurrentTimesheetViewer()
    main_window.show()
    sys.exit(app.exec_())
