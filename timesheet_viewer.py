import sys

from PySide2.QtWidgets import QDialog, QGridLayout, QCalendarWidget, QApplication


class Viewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.cal = Calendar()

        grid_layout.addWidget(self.cal)


class Calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Viewer()
    main_window.show()
    sys.exit(app.exec_())
