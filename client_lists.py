# TODO Fix vertical resizing issues
import functools
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QListWidget,
    QLabel,
    QApplication,
    QGridLayout,
    QPushButton,
    QAbstractItemView,
    QLineEdit,
    QHBoxLayout,
    QFrame,
    QDialogButtonBox,
    QDialog,
)

from populate_db import (
    show_clients,
    show_all_clients,
    activate_client,
    enter_client,
    inactivate_client,
)


class ClientList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Client List")
        self.setMinimumWidth(630)
        self.setMinimumHeight(320)

        self.active_clients = ClientListWidget()
        self.active_clients.addItems(show_clients(active=True))
        self.inactive_clients = ClientListWidget()
        self.inactive_clients.addItems(show_clients(active=False))

        self.move_left = QPushButton("<-")
        self.move_left.clicked.connect(
            functools.partial(
                self.move_items, self.inactive_clients, self.active_clients
            )
        )
        self.move_right = QPushButton("->")
        self.move_right.clicked.connect(
            functools.partial(
                self.move_items, self.active_clients, self.inactive_clients
            )
        )

        add_client_row = QHBoxLayout()
        self.new_client_name = QLineEdit()
        self.add_client_button = QPushButton("Add Client")
        self.add_client_button.clicked.connect(self.add_to_active_clients)
        add_client_row.addWidget(self.new_client_name)
        add_client_row.addWidget(self.add_client_button)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.update_client_db)
        self.button_box.rejected.connect(self.close)

        self.active_label = QLabel("Active Clients")
        self.inactive_label = QLabel("Inactive Clients")

        grid_layout = QGridLayout(self)
        grid_layout.addLayout(add_client_row, 0, 0, 1, 2)
        grid_layout.addWidget(QHLine(), 1, 0, 1, 3)
        grid_layout.addWidget(self.active_label, 2, 0)
        grid_layout.addWidget(self.inactive_label, 2, 2)
        grid_layout.addWidget(self.active_clients, 3, 0, 2, 1)
        grid_layout.addWidget(self.move_left, 3, 1, 1, 1, Qt.AlignBottom)
        grid_layout.addWidget(self.move_right, 4, 1, 1, 1, Qt.AlignTop)
        grid_layout.addWidget(self.inactive_clients, 3, 2, 2, 1)
        grid_layout.addWidget(QHLine(), 5, 0, 1, 3)
        grid_layout.addWidget(self.button_box, 6, 0, 1, 3, Qt.AlignCenter)

    def update_client_db(self):
        # TODO bulk inserstion of database. Currently each client in the list is a db commit
        all_clients = show_all_clients()
        active_clients = [
            self.active_clients.item(i).text()
            for i in range(self.active_clients.count())
        ]
        inactive_clients = [
            self.inactive_clients.item(i).text()
            for i in range(self.inactive_clients.count())
        ]
        for client in active_clients:
            if client in all_clients:
                activate_client(client)
            else:
                enter_client(client)
        for client in inactive_clients:
            if client in all_clients:
                inactivate_client(client)
            else:
                enter_client(client)
                inactivate_client(client)
        # Refresh the Timer Widget in the QMainWindow to show the new active and inactive clients
        # Consider adding a signal/slot for this behavior
        self.parent().timer_widget.combo_box.clear()
        self.parent().timer_widget.combo_box.addItems(show_clients(active=True))
        self.parent().timer_widget.combo_box.setCurrentIndex(-1)
        self.close()

    def move_items(self, original_list, new_list):
        for item in original_list.selectedItems():
            original_list.takeItem(original_list.row(item))
            new_list.addItem(item.text())

    def add_to_active_clients(self):
        self.active_clients.addItem(self.new_client_name.text())
        self.new_client_name.clear()


class ClientListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setMinimumSize(40, 200)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ClientList()
    main_window.show()
    print(main_window.geometry().width())
    print(main_window.geometry().height())
    sys.exit(app.exec())
