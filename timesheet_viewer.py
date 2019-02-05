import sys
from datetime import timedelta
from populate_db import retrieve_time

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

import pandas as pd


class Viewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)
        self.date_picker = DatePicker()
        self.date_picker.dateChanged.connect(self.show_date)
        self.date_label = QLabel()
        self.date_label.setText("Pick a Date")
        self.ok_btn = QPushButton("Push Button")
        self.ok_btn.clicked.connect(self.button_clicked)
        grid_layout.addWidget(self.date_label, 0, 0)
        grid_layout.addWidget(self.date_picker, 1, 0)
        grid_layout.addWidget(self.ok_btn, 2, 0)

    def show_date(self, date):
        self.date_label.setText(date.toString())

    def button_clicked(self):
        start_date = self.date_picker.date().toPython()
        end_date = start_date + timedelta(days=5)
        results = retrieve_time(start_date, end_date)
        dframe_days = pd.date_range(start=start_date, periods=5)
        df = pd.read_sql(
            results.statement,
            results.session.bind,
            parse_dates=["day"],
            index_col=["name"],
        ).drop(["id"], axis=1)
        df = df.groupby(["name", "day"])["total_time"].sum().unstack(fill_value=0)
        print(df)
        print()
        end_result = df.to_dict()
        print(end_result)
        new_df = pd.DataFrame.from_dict(end_result)
        print(new_df)
        # writer = pd.ExcelWriter("saved.xlsx", engine="xlsxwriter", date_format="dddd mmmm dd yyyy", datetime_format="dddd mmmm dd yyyy")
        # new_df.to_excel(writer)
        # writer.save()


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
