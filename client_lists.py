import sys

from PySide2.QtWidgets import QListWidget, QWidget, QApplication, QListWidgetItem, QGridLayout, QPushButton, \
    QVBoxLayout, QAbstractItemView


class ClientList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = QGridLayout(self)

        self.selected_clients = QListWidget()
        self.selected_clients.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selected_clients.addItems(['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', ])
        self.all_clients = QListWidget()

        self.move_left = QPushButton('<-')
        self.move_left.clicked.connect(self.move_items_left)
        self.move_right = QPushButton('->')
        self.move_right.clicked.connect(self.move_items_right)


        grid_layout.addWidget(self.selected_clients, 0, 0)
        grid_layout.addWidget(self.move_left, 0, 1)
        grid_layout.addWidget(self.move_right,1, 1)
        grid_layout.addWidget(self.all_clients, 0, 2)

    def print_items(self):
        items = self.selected_clients.selectedItems()
        for item in items:
            print(item.text())

    def move_items_left(self):
        for item in self.all_clients.selectedItems():
            self.all_clients.takeItem(self.all_clients.row(item))
            self.selected_clients.addItem(item.text())


    def move_items_right(self):
        for item in self.selected_clients.selectedItems():
            self.selected_clients.takeItem(self.selected_clients.row(item))
            self.all_clients.addItem(item.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ClientList()
    main_window.show()
    sys.exit(app.exec_())

