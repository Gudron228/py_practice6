import sys
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListView, QLabel


class Product:
    def __init__(self, name, quantity, weight_per_unit):
        self.name = name
        self.quantity = quantity
        self.weight_per_unit = weight_per_unit


class ProductListModel(QAbstractListModel):
    def __init__(self, products=None):
        super().__init__()
        self.products = products or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.products)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            product = self.products[index.row()]
            return f"{product.name}: {product.quantity} x {product.weight_per_unit}kg"
        return None

    def add_product(self, product):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.products.append(product)
        self.endInsertRows()

    def total_weight(self):
        return sum(product.quantity * product.weight_per_unit for product in self.products)


class ProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список продуктов")
        layout = QVBoxLayout()

        self.product_model = ProductListModel()

        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.weight_input = QLineEdit()

        self.name_input.setPlaceholderText("Название продукта")
        self.quantity_input.setPlaceholderText("Количество")
        self.weight_input.setPlaceholderText("Вес (кг)")

        layout.addWidget(self.name_input)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.weight_input)

        add_button = QPushButton("Добавить продукт")
        add_button.clicked.connect(self.add_product)
        layout.addWidget(add_button)

        self.products_list = QListView()
        self.products_list.setModel(self.product_model)
        layout.addWidget(self.products_list)

        self.total_weight_label = QLabel()
        layout.addWidget(self.total_weight_label)

        self.setLayout(layout)

    def add_product(self):
        name = self.name_input.text()
        quantity = int(self.quantity_input.text())
        weight_per_unit = float(self.weight_input.text())

        product = Product(name, quantity, weight_per_unit)
        self.product_model.add_product(product)
        self.update_total_weight()

    def update_total_weight(self):
        total_weight = self.product_model.total_weight()
        self.total_weight_label.setText(f"Общий вес: {total_weight} кг")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(app.exec())
