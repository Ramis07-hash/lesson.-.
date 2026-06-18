import sqlite3


# =========================
# DATABASE CONNECTION
# =========================

connection = sqlite3.connect("academy.db")
cursor = connection.cursor()


# =========================
# CREATE TABLES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    teacher TEXT
)
""")


# MANY TO MANY RELATION
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_courses (
    student_id INTEGER,
    course_id INTEGER,

    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

connection.commit()


# =========================
# STUDENT CRUD
# =========================

def create_student():

    name = input("Student name: ")
    age = int(input("Student age: "))
    email = input("Student email: ")

    cursor.execute("""
    INSERT INTO students(name, age, email)
    VALUES (?, ?, ?)
    """, (name, age, email))

    connection.commit()

    print("Student added successfully!")


def read_students():

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    print("\n===== STUDENTS =====")

    for student in students:
        print(student)


def update_student():

    student_id = int(input("Enter student ID: "))

    new_name = input("New name: ")
    new_age = int(input("New age: "))
    new_email = input("New email: ")

    cursor.execute("""
    UPDATE students
    SET name = ?, age = ?, email = ?
    WHERE id = ?
    """, (new_name, new_age, new_email, student_id))

    connection.commit()

    print("Student updated successfully!")


def delete_student():

    student_id = int(input("Enter student ID: "))

    cursor.execute("""
    DELETE FROM students
    WHERE id = ?
    """, (student_id,))

    connection.commit()

    print("Student deleted successfully!")


# =========================
# COURSE CRUD
# =========================

def create_course():

    course_name = input("Course name: ")
    teacher = input("Teacher name: ")

    cursor.execute("""
    INSERT INTO courses(course_name, teacher)
    VALUES (?, ?)
    """, (course_name, teacher))

    connection.commit()

    print("Course added successfully!")


def read_courses():

    cursor.execute("SELECT * FROM courses")

    courses = cursor.fetchall()

    print("\n===== COURSES =====")

    for course in courses:
        print(course)


def update_course():

    course_id = int(input("Enter course ID: "))

    new_course_name = input("New course name: ")
    new_teacher = input("New teacher name: ")

    cursor.execute("""
    UPDATE courses
    SET course_name = ?, teacher = ?
    WHERE id = ?
    """, (new_course_name, new_teacher, course_id))

    connection.commit()

    print("Course updated successfully!")


def delete_course():

    course_id = int(input("Enter course ID: "))

    cursor.execute("""
    DELETE FROM courses
    WHERE id = ?
    """, (course_id,))

    connection.commit()

    print("Course deleted successfully!")


# =========================
# ENROLL STUDENT TO COURSE
# =========================

def enroll_student():

    student_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))

    cursor.execute("""
    INSERT INTO student_courses(student_id, course_id)
    VALUES (?, ?)
    """, (student_id, course_id))

    connection.commit()

    print("Student enrolled successfully!")


def show_student_courses():

    cursor.execute("""
    SELECT students.name, courses.course_name
    FROM student_courses
    JOIN students
        ON student_courses.student_id = students.id
    JOIN courses
        ON student_courses.course_id = courses.id
    """)

    data = cursor.fetchall()

    print("\n===== STUDENT COURSES =====")

    for row in data:
        print(f"Student: {row[0]} -> Course: {row[1]}")


# =========================
# MENU
# =========================

while True:

    print("""
======== MENU ========

1. Add Student
2. Show Students
3. Update Student
4. Delete Student

5. Add Course
6. Show Courses
7. Update Course
8. Delete Course

9. Enroll Student To Course
10. Show Student Courses

0. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        create_student()

    elif choice == "2":
        read_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        create_course()

    elif choice == "6":
        read_courses()

    elif choice == "7":
        update_course()

    elif choice == "8":
        delete_course()

    elif choice == "9":
        enroll_student()

    elif choice == "10":
        show_student_courses()

    elif choice == "0":
        print("Program finished!")
        break

    else:
        print("Wrong choice!")