import sys
import sqlite3
# Иштөөсү үчүн PyQt6 колдонобуз
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QLineEdit, 
    QComboBox, QPushButton, QMessageBox, QHeaderView
)

# =====================================================================
# БАЗА МЕНЕН ИШТӨӨ КЛАССЫ
# =====================================================================
class MovieDatabase:
    def __init__(self, db_name="movies.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """3 колонкалуу таблица түзөт."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                year TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add(self, title, genre, year):
        """Биздин базага жаңы маалымат кошот."""
        self.cursor.execute(
            "INSERT INTO movies (title, genre, year) VALUES (?, ?, ?)",
            (title, genre, year)
        )
        self.conn.commit()

    def get_all(self):
        """Базадагы бардык маалыматтарды кайтарат."""
        self.cursor.execute("SELECT title, genre, year FROM movies")
        return self.cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


# =====================================================================
# ТИРКЕМЕНИН ТЕРЕЗЕ КЛАССЫ
# =====================================================================
class MovieApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MovieDatabase()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Фильмдер жыйнагы (PyQt6)")
        self.resize(550, 400)

        main_layout = QVBoxLayout()

        # Маалыматтарды көрсөтүүчү таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Аталышы", "Жанры", "Чыккан жылы"])
        
        # PyQt6-да таблицанын четтерин созуу форматы
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.table)

        # Төмөнкү бөлүктөгү форма (Жаткан сызык)
        form_layout = QHBoxLayout()

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Фильмдин аты...")
        
        self.combo_genre = QComboBox()
        self.combo_genre.addItems(["Фантастика", "Боевик", "Комедия", "Драма", "Ужасы", "Аниме"])

        self.input_year = QLineEdit()
        self.input_year.setPlaceholderText("Жылы...")
        self.input_year.setMaximumWidth(80)

        btn_add = QPushButton("Кошуу")
        btn_add.clicked.connect(self.handle_add_movie)

        form_layout.addWidget(self.input_title)
        form_layout.addWidget(self.combo_genre)
        form_layout.addWidget(self.input_year)
        form_layout.addWidget(btn_add)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

    def load_data(self):
        """Базадан маалыматты алып, таблицаны жаңылайт."""
        self.table.setRowCount(0)
        movies = self.db.get_all()
        
        for row_idx, movie_data in enumerate(movies):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(movie_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def handle_add_movie(self):
        """Баскыч басылгандагы логика."""
        title = self.input_title.text().strip()
        genre = self.combo_genre.currentText()
        year = self.input_year.text().strip()

        # Бош талааларды текшерүү (Валидация)
        if not title or not year:
            QMessageBox.critical(
                self, 
                "Ката", 
                "Сураныч, бардык талааларды толтуруңуз (Аты жана Жылы)!"
            )
            return

        # Базага сактоо
        self.db.add(title, genre, year)

        # Жазуу талааларын тазалоо
        self.input_title.clear()
        self.input_year.clear()

        # Таблицаны жаңылоо
        self.load_data()


# =====================================================================
# ПРОГРАММАНЫ ИШКЕ КИРГИЗҮҮ
# =====================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieApp()
    window.show()
    sys.exit(app.exec())
