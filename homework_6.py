import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        # Фиксированные курсы валют
        self.rates = {
            "USD": 1.0,
            "EUR": 1.2,
            "KGS": 87.0
        }
        self.init_ui()

    def init_ui(self):
        # 1. Настройки главного окна
        self.setWindowTitle("Конвертер валют")
        self.setMinimumSize(400, 300)

        # 2. Создание элементов интерфейса
        self.label_input = QLabel("Введите сумму (USD):")
        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Например: 100")

        self.btn_to_kgs = QPushButton("Конвертировать в KGS")
        self.btn_to_eur = QPushButton("Конвертировать в EUR")
        self.btn_clear = QPushButton("Очистить")

        self.label_result = QLabel("Результат: 0.00")
        # Выравнивание текста по центру и стилизация для улучшения видимости
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")

        # 3. Подключение функций к кнопкам (События)
        self.btn_to_kgs.clicked.connect(lambda: self.convert_currency("KGS"))
        self.btn_to_eur.clicked.connect(lambda: self.convert_currency("EUR"))
        self.btn_clear.clicked.connect(self.clear_fields)

        # 4. Расположение элементов (Layouts)
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Размещение кнопок конвертации в один горизонтальный ряд
        button_layout.addWidget(self.btn_to_kgs)
        button_layout.addWidget(self.btn_to_eur)

        # Добавление всех элементов в главный вертикальный контейнер
        main_layout.addWidget(self.label_input)
        main_layout.addWidget(self.input_amount)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.btn_clear)
        main_layout.addStretch()  # Пружина для распределения пространства
        main_layout.addWidget(self.label_result)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def convert_currency(self, target_currency):
        # Получение текста из поля ввода
        text = self.input_amount.text().strip()

        # Валидация данных и обработка ошибок
        try:
            # Заменяем запятую на точку, если пользователь ввел ее как разделитель
            text = text.replace(',', '.')
            amount = float(text)
            
            if amount < 0:
                raise ValueError("Сумма не может быть отрицательной")
                
        except ValueError:
            # Показ сообщения об ошибке при некорректном вводе
            QMessageBox.critical(
                self, 
                "Ошибка ввода", 
                "Некорректное значение! Пожалуйста, введите число (например: 100 или 50.5)."
            )
            return

        # Логика конвертации по заданной формуле
        source_currency = "USD"
        rate_source = self.rates[source_currency]
        rate_target = self.rates[target_currency]
        
        # Формула: результат = сумма * (курс_целевой / курс_исходной)
        result = amount * (rate_target / rate_source)

        # Вывод результата с двумя знаками после запятой
        self.label_result.setText(f"Результат: {result:.2f} {target_currency}")

    def clear_fields(self):
        # Очистка поля ввода и сброс текста результата
        self.input_amount.clear()
        self.label_result.setText("Результат: 0.00")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec())
