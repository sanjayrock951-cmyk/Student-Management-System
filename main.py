import os
import sqlite3
from database import create_database, DB_PATH

DB_NAME = DB_PATH


def add_student():
    print("\n--- Add New Student ---")
    name = input("Enter student name: ").strip()
    age = input("Enter age: ").strip()
    course = input("Enter course: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()

    if not all([name, age, course, email, phone]):
        print("Error: All fields are required.")
        return

    try:
        age = int(age)
        if age <= 0:
            print("Age must be greater than zero.")
            return

        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT INTO students (name, age, course, email, phone)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, course, email, phone))

        print("Student added successfully!")

    except ValueError:
        print("Error: Age must be a number.")
    except sqlite3.IntegrityError:
        print("Error: This email is already registered.")


def view_students():
    with sqlite3.connect(DB_NAME) as conn:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

    print("\n--- All Students ---")
    if not students:
        print("No students registered yet.")
        return

    for student in students:
        print("-" * 35)
        print(f"ID: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Age: {student[2]}")
        print(f"Course: {student[3]}")
        print(f"Email: {student[4]}")
        print(f"Phone: {student[5]}")


def search_student():
    student_id = input("Enter student ID to search: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid numeric ID.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (int(student_id),)
        ).fetchone()

    if student:
        print("\nStudent found:")
        print(student)
    else:
        print("Student not found.")


def update_student():
    student_id = input("Enter student ID to update: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid numeric ID.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (int(student_id),)
        ).fetchone()

        if not student:
            print("Student not found.")
            return

        print("Press Enter to keep the existing value.")

        name = input(f"Name [{student[1]}]: ").strip() or student[1]
        age_input = input(f"Age [{student[2]}]: ").strip()
        course = input(f"Course [{student[3]}]: ").strip() or student[3]
        email = input(f"Email [{student[4]}]: ").strip() or student[4]
        phone = input(f"Phone [{student[5]}]: ").strip() or student[5]

        try:
            age = int(age_input) if age_input else student[2]
            if age <= 0:
                print("Age must be greater than zero.")
                return

            conn.execute("""
                UPDATE students
                SET name=?, age=?, course=?, email=?, phone=?
                WHERE id=?
            """, (name, age, course, email, phone, int(student_id)))

            print("Student updated successfully.")

        except ValueError:
            print("Age must be a number.")
        except sqlite3.IntegrityError:
            print("This email is already registered.")

def delete_student():
    student_id = input("Enter student ID to delete: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid numeric ID.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (int(student_id),)
        )

        if cursor.rowcount > 0:
            print("Student deleted successfully.")
        else:
            print("Student ID not found in this database.")


def main():
    create_database()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Update Student")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
         add_student()
        elif choice == "2":
         view_students()
        elif choice == "3":
         search_student()
        elif choice == "4":
         delete_student()
        elif choice == "5":
         update_student()
        elif choice == "6":
         print("Thank you for using Student Management System!")
        break
    else:
     print("Invalid choice. Please select 1 to 6.")
            
        
            
        
            
        
            
        
            
            
        
        


if __name__ == "__main__":
    main()
