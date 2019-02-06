import sys

import pandas as pd
from PySide2.QtCore import QDate, Qt
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QCalendarWidget,
    QApplication,
    QLabel,
    QDateEdit,
    QPushButton,
)

from populate_db import retrieve_time


class Viewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.start_date_picker = DatePicker()
        self.start_date_picker.dateChanged.connect(self.start_date_chosen)
        self.end_date_picker = DatePicker()
        self.end_date_picker.setDate(QDate.currentDate().addDays(6))
        self.end_date_picker.setMinimumDate(QDate.currentDate())
        self.start_date_label = QLabel()
        self.start_date_label.setText("Start Date")
        self.end_date_label = QLabel()
        self.end_date_label.setText("End Date")
        self.ok_btn = QPushButton("Save to Excel")
        self.ok_btn.clicked.connect(self.button_clicked)
        grid_layout.addWidget(self.start_date_label, 0, 0)
        grid_layout.addWidget(self.end_date_label, 0, 1)
        grid_layout.addWidget(self.start_date_picker, 1, 0)
        grid_layout.addWidget(self.end_date_picker, 1, 1)
        grid_layout.addWidget(self.ok_btn, 2, 0, 1, 2, alignment=Qt.AlignCenter)

    def start_date_chosen(self, date):
        self.end_date_picker.setDate(date.addDays(6))
        self.end_date_picker.setMinimumDate(date)

    def button_clicked(self):
        start_date = self.start_date_picker.date().toPython()
        end_date = self.end_date_picker.date().toPython()
        results = retrieve_time(start_date, end_date)
        df = pd.read_sql(
            results.statement,
            results.session.bind,
            parse_dates=["day"],
            index_col=["name"],
        ).drop(["id"], axis=1)
        df = df.groupby(["name", "day"])["total_time"].sum().unstack(fill_value=0)
        writer = pd.ExcelWriter(
            "saved.xlsx",
            engine="xlsxwriter",
            date_format="dddd mmm dd yy",
            datetime_format="dddd mmm dd yy",
        )
        df.to_excel(writer)
        writer.save()


class DatePicker(QDateEdit):
    def __init__(self):
        super().__init__()
        self.setDisplayFormat("dd/MM/yy")
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
