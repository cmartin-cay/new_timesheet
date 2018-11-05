import functools
import sys
from populate_db import show_clients, show_all_clients, activate_client, enter_client, inactivate_client

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QListWidget, QWidget, QApplication, QGridLayout, QPushButton, QAbstractItemView, \
    QLineEdit, QHBoxLayout, QFrame, QDialogButtonBox


class ClientList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)

        # self.selected_clients = QListWidget()
        # self.selected_clients.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.active_clients = ClientListWidget()
        self.active_clients.addItems(show_clients(active=True))
        self.inactive_clients = ClientListWidget()
        self.inactive_clients.addItems(show_clients(active=False))

        self.move_left = QPushButton('<-')
        self.move_left.clicked.connect(functools.partial(self.move_items, self.inactive_clients, self.active_clients))
        self.move_right = QPushButton('->')
        self.move_right.clicked.connect(functools.partial(self.move_items, self.active_clients, self.inactive_clients))

        add_client_row = QHBoxLayout()
        self.new_client_name = QLineEdit()
        self.add_client_button = QPushButton("Add Client")
        self.add_client_button.clicked.connect(self.add_to_active_clients)
        add_client_row.addWidget(self.new_client_name)
        add_client_row.addWidget(self.add_client_button)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.update_client_db)
        self.button_box.rejected.connect(self.close)

        grid_layout.addLayout(add_client_row, 0, 0, 1, 2)
        grid_layout.addWidget(QHLine(), 1, 0, 1, 3)
        grid_layout.addWidget(self.active_clients, 2, 0, 2, 1)
        grid_layout.addWidget(self.move_left, 2, 1, 1, 1, Qt.AlignBottom)
        grid_layout.addWidget(self.move_right, 3, 1, 1, 1, Qt.AlignTop)
        grid_layout.addWidget(self.inactive_clients, 2, 2, 2, 1)
        grid_layout.addWidget(self.button_box, 4, 0, 1, 3, Qt.AlignCenter)

    def update_client_db(self):
        # TODO bulk inserstion of database. Currently each client in the list is a db commit
        all_clients = show_all_clients()
        active_clients = [self.active_clients.item(i).text() for i in range(self.active_clients.count())]
        inactive_clients = [self.inactive_clients.item(i).text() for i in range(self.inactive_clients.count())]
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
    sys.exit(app.exec_())
