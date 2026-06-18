import sys
import sqlite3

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget
)

db = sqlite3.connect("students.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course INTEGER,
    debt INTEGER,
    reason TEXT
)
""")

db.commit()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("База должников 😈")
        self.resize(500, 600)

        layout = QVBoxLayout()

        title = QLabel("Добавить студента")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Курс")

        self.debt_input = QLineEdit()
        self.debt_input.setPlaceholderText("Долг")

        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("Причина долга")

        self.add_btn = QPushButton("Добавить студента")

        self.students_list = QListWidget()

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.course_input)
        layout.addWidget(self.debt_input)
        layout.addWidget(self.reason_input)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.students_list)

        self.setLayout(layout)

        self.add_btn.clicked.connect(self.add_student)

        self.load_students()

    def add_student(self):
        name = self.name_input.text()
        age = self.age_input.text()
        course = self.course_input.text()
        debt = self.debt_input.text()
        reason = self.reason_input.text()

        if not all([name, age, course, debt, reason]):
            return

        cursor.execute("""
        INSERT INTO students (
            name,
            age,
            course,
            debt,
            reason
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            age,
            course,
            debt,
            reason
        ))

        db.commit()

        self.name_input.clear()
        self.age_input.clear()
        self.course_input.clear()
        self.debt_input.clear()
        self.reason_input.clear()

        self.load_students()

    def load_students(self):
        self.students_list.clear()

        cursor.execute("""
        SELECT
            name,
            age,
            course,
            debt,
            reason
        FROM students
        """)

        students = cursor.fetchall()

        for student in students:
            name, age, course, debt, reason = student

            if int(debt) > 10000:
                status = "🚨 Опасный должник"
            else:
                status = "✅ Еще можно спасти"

            text = (
                f"{name} | "
                f"{age} лет | "
                f"{course} курс | "
                f"{debt} сом | "
                f"{reason} | "
                f"{status}"
            )

            self.students_list.addItem(text)


app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())