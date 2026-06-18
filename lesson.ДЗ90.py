import sqlite3
import time
from abc import ABC, abstractmethod
from functools import wraps


# =========================
# DATABASE
# =========================

connection = sqlite3.connect("academy.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    name TEXT,
    email TEXT
)
""")

connection.commit()


# =========================
# DECORATORS
# =========================

def log_action(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        print(f"\n[LOG] Function: {func.__name__}")

        result = func(*args, **kwargs)

        end = time.time()

        print(f"[LOG] Time: {end - start:.4f} sec")

        return result

    return wrapper


def admin_required(func):

    @wraps(func)
    def wrapper(user, *args, **kwargs):

        if not getattr(user, "is_admin", False):
            print("ACCESS DENIED! ONLY ADMIN!")
            return

        return func(user, *args, **kwargs)

    return wrapper


# =========================
# ABSTRACT CLASS
# =========================

class User(ABC):

    @abstractmethod
    def login(self):
        pass


# =========================
# MIXINS
# =========================

class NotificationMixin:

    def send_notification(self, message):
        print(f"[NOTIFICATION]: {message}")


class LoggerMixin:

    def log(self, message):
        print(f"[LOGGER]: {message}")


# =========================
# PERSON CLASS
# =========================

class Person(User):

    def __init__(self, name, email, password):

        # PUBLIC
        self.name = name

        # PROTECTED
        self._balance = 0

        # PRIVATE
        self.__password = password

        self.email = email

    def login(self):
        return f"{self.name} logged in"

    def check_password(self, password):
        return self.__password == password

    def get_info(self):
        return f"Person: {self.name}"


# =========================
# STUDENT CLASS
# =========================

class Student(Person):

    def __init__(self, student_id, name, email, password):

        super().__init__(name, email, password)

        self.student_id = student_id

    # POLYMORPHISM
    def get_info(self):
        return f"Student -> ID: {self.student_id}, Name: {self.name}"

    # MAGIC METHODS
    def __str__(self):
        return f"Student({self.name})"

    def __repr__(self):
        return f"Student('{self.student_id}', '{self.name}')"

    def __eq__(self, other):
        return self.student_id == other.student_id

    # STATIC METHOD
    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

    # CLASS METHOD
    @classmethod
    def from_string(cls, data):

        student_id, name, email, password = data.split(",")

        return cls(student_id, name, email, password)


# =========================
# TEACHER CLASS
# =========================

class Teacher(Person, NotificationMixin, LoggerMixin):

    def __init__(self, teacher_id, name, email, password):

        super().__init__(name, email, password)

        self.teacher_id = teacher_id

    # POLYMORPHISM
    def get_info(self):
        return f"Teacher -> ID: {self.teacher_id}, Name: {self.name}"


# =========================
# ADMIN CLASS
# =========================

class Admin(Person):

    def __init__(self, admin_id, name, email, password):

        super().__init__(name, email, password)

        self.admin_id = admin_id

        self.is_admin = True

    # POLYMORPHISM
    def get_info(self):
        return f"Admin -> {self.name}"


# =========================
# COURSE CLASS
# =========================

class Course:

    def __init__(self, title):

        self.title = title

        self.students = []

    def add_student(self, student):
        self.students.append(student)

    # MAGIC METHOD
    def __len__(self):
        return len(self.students)

    def __str__(self):
        return f"Course({self.title})"

    def __repr__(self):
        return f"Course('{self.title}')"


# =========================
# SERVICES
# =========================

class StudentService:

    @staticmethod
    @log_action
    def add_student(student):

        cursor.execute(
            """
            INSERT INTO students(student_id, name, email)
            VALUES (?, ?, ?)
            """,
            (student.student_id, student.name, student.email)
        )

        connection.commit()

        print("Student added to database!")

    @staticmethod
    @log_action
    def show_students():

        cursor.execute("SELECT * FROM students")

        students = cursor.fetchall()

        print("\nDATABASE STUDENTS:")

        for student in students:
            print(student)


class CourseService:

    @staticmethod
    @log_action
    def enroll_student(course, student):

        course.add_student(student)

        print(f"{student.name} enrolled to {course.title}")


# =========================
# ADMIN FUNCTION
# =========================

@admin_required
def delete_student(user):

    print("Student deleted successfully!")


# =========================
# MAIN PROGRAM
# =========================

print("\n===== ACADEMY MANAGEMENT SYSTEM =====")


# OBJECTS
student1 = Student(
    "S101",
    "Ali",
    "ali@gmail.com",
    "1234"
)

student2 = Student.from_string(
    "S102,Aibek,aibek@gmail.com,5555"
)

teacher1 = Teacher(
    "T201",
    "John",
    "john@gmail.com",
    "1111"
)

admin1 = Admin(
    "A1",
    "Boss",
    "boss@gmail.com",
    "9999"
)


# LOGIN
print("\nLOGIN:")
print(student1.login())


# POLYMORPHISM
print("\nGET INFO:")
print(student1.get_info())
print(teacher1.get_info())
print(admin1.get_info())


# STATIC METHOD
print("\nEMAIL VALIDATION:")
print(Student.validate_email("test@gmail.com"))


# MAGIC METHODS
print("\nMAGIC METHODS:")
print(student1)
print(repr(student1))
print(student1 == student2)


# COURSE
python_course = Course("Python Backend")

CourseService.enroll_student(
    python_course,
    student1
)

CourseService.enroll_student(
    python_course,
    student2
)

print(f"\nStudents count in course: {len(python_course)}")


# DATABASE
StudentService.add_student(student1)
StudentService.add_student(student2)

StudentService.show_students()


# MULTIPLE INHERITANCE
print("\nMIXINS:")
teacher1.send_notification("Lesson starts at 18:00")
teacher1.log("Teacher entered system")


# ADMIN DECORATOR
print("\nADMIN CHECK:")
delete_student(admin1)
delete_student(student1)


print("\n===== PROGRAM FINISHED =====")