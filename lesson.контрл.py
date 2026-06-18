import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel
)


class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список студентов")
        self.resize(400, 300)

        layout = QVBoxLayout()

        
        layout.addWidget(QLabel("Имя студента:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Кнопка
        self.add_button = QPushButton("Добавить")
        layout.addWidget(self.add_button)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Имя студента"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Событие кнопки
        self.add_button.clicked.connect(self.add_student)

    def add_student(self):
        name = self.name_input.text().strip()

        if name:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(name)
            )

            # Очистить поле
            self.name_input.clear()


app = QApplication(sys.argv)
window = StudentWindow()
window.show()
sys.exit(app.exec())