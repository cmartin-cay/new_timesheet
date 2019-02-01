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
            # index_col=["name"]
        ).drop(["id"], axis=1)
        print(df)
        print()
        dframe = pd.pivot_table(df, index=["name"], aggfunc=sum)
        print(dframe)
        df = pd.DataFrame(dframe.to_records())
        print(df)
        writer = pd.ExcelWriter("saved.xlsx")
        dframe.to_excel(writer)
        writer.save()



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
