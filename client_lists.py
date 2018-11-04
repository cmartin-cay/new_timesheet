import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QListWidget, QWidget, QApplication, QGridLayout, QPushButton, QAbstractItemView, \
    QFormLayout, QLineEdit, QLabel, QHBoxLayout
import functools


class ClientList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)

        # self.selected_clients = QListWidget()
        # self.selected_clients.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.active_clients = ClientListWidget()
        self.active_clients.addItems(['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'])
        self.inactive_clients = ClientListWidget()


        self.move_left = QPushButton('<-')
        self.move_left.clicked.connect(functools.partial(self.move_items, self.inactive_clients, self.active_clients))
        self.move_right = QPushButton('->')
        self.move_right.clicked.connect(functools.partial(self.move_items, self.active_clients, self.inactive_clients))

        add_client_row = QHBoxLayout()
        self.new_client_name = QLineEdit()
        self.add_client_button  = QPushButton("Add Client")
        add_client_row.addWidget(self.new_client_name)
        add_client_row.addWidget(self.add_client_button)

        grid_layout.addLayout(add_client_row, 2, 0, 1, 2)
        grid_layout.addWidget(self.active_clients, 0, 0, 2, 1)
        grid_layout.addWidget(self.move_left, 0, 1, 1, 1, Qt.AlignBottom)
        grid_layout.addWidget(self.move_right,1, 1, 1, 1, Qt.AlignTop)
        grid_layout.addWidget(self.inactive_clients, 0, 2, 2, 1)

    def print_items(self):
        items = self.active_clients.selectedItems()
        for item in items:
            print(item.text())

    def move_items(self, original_list, new_list):
        for item in original_list.selectedItems():
            original_list.takeItem(original_list.row(item))
            new_list.addItem(item.text())


    def move_items_right(self):
        for item in self.active_clients.selectedItems():
            self.active_clients.takeItem(self.active_clients.row(item))
            self.inactive_clients.addItem(item.text())

class ClientListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setMinimumSize(40,200)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ClientList()
    main_window.show()
    sys.exit(app.exec_())

