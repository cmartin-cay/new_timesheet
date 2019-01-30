import sys

from PySide2.QtCore import QDate, Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QCalendarWidget, QApplication, QLabel, QDateEdit


class Viewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.date_picker = DatePicker()
        self.date_picker.dateChanged.connect(self.show_date)
        self.date_label = QLabel()
        self.date_label.setText("Pick a Date")
        grid_layout.addWidget(self.date_label, 0, 0)
        grid_layout.addWidget(self.date_picker, 1, 0)

    def show_date(self, date):
        self.date_label.setText(date.toString())


class DatePicker(QDateEdit):
    def __init__(self):
        super().__init__()
        self.setDate(QDate.currentDate())
        self.setCalendarPopup(True)
        self.setCalendarWidget(Calendar())

class Calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.setGridVisible(True)
        self.setFirstDayOfWeek(Qt.Monday)
        self.setVerticalHeaderFormat(self.NoVerticalHeader)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Viewer()
    main_window.show()
    sys.exit(app.exec_())
