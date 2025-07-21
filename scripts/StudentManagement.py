import psycopg2

def print_all_students(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY id;")
    rows = cur.fetchall()
    print("\n📋 Current Students:")
    for row in rows:
        id, name, email, class_number, overall_grade = row
        print(f"ID: {id} | Name: {name} | Email: {email} | Class: {class_number} | Grade: {overall_grade}")
    print("-" * 60)
    cur.close()

def view_comments(conn):
    try:
        student_id = int(input("Enter the student ID to view comments: "))
        cur = conn.cursor()
        cur.execute("""
            SELECT s.name, c.comment, c.created_on 
            FROM notes_comments c
            JOIN students s ON c.student_id = s.id
            WHERE c.student_id = %s
            ORDER BY c.created_on DESC;
        """, (student_id,))
        rows = cur.fetchall()

        if not rows:
            print("❗ No comments found for this student.")
        else:
            print(f"\n📝 Comments for Student ID {student_id}:")
            for name, comment, created_on in rows:
                print(f"{created_on} | {name}: {comment}")
        print("-" * 60)
        cur.close()
    except Exception as error:
        print("❌ Error viewing comments:", error)

def view_subjects(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM subjects")
        rows = cur.fetchall()
        print("\n📚 Available Subjects:")
        for subject_id, name in rows:
            print(f"{subject_id}. {name}")
        print("-" * 60)
        cur.close()
    except Exception as e:
        print("❌ Could not fetch subjects:", e)

def add_grade(conn):
    try:
        student_id = int(input("Enter student ID: "))
        view_subjects(conn)
        subject_id = int(input("Enter subject ID: "))
        grade = input("Enter grade (A-F): ").upper()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO grades (student_id, subject_id, grade)
            VALUES (%s, %s, %s);
        """, (student_id, subject_id, grade))
        conn.commit()
        print("✅ Grade added.")
        cur.close()
    except Exception as e:
        print("❌ Error adding grade:", e)

def add_student(conn):
    name = input("Enter full name: ")
    email = input("Enter email: ")
    class_number = input("Enter class: ")
    overall_grade = input("Enter overall grade (A-F): ").upper()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO students (name, email, class_number, overall_grade)
            VALUES (%s, %s, %s, %s);
        """, (name, email, class_number, overall_grade))
        conn.commit()
        print(f"\n✅ Student {name} added successfully.")
        cur.close()
    except Exception as error:
        print("❌ Error appending student...", error)

def delete_student(conn):
    try:
        student_id = int(input("Enter the ID of the student to delete: "))
        cur = conn.cursor()
        cur.execute("DELETE FROM attendance WHERE student_id = %s;", (student_id,))
        cur.execute("DELETE FROM grades WHERE student_id = %s;", (student_id,))
        cur.execute("DELETE FROM notes_comments WHERE student_id = %s;", (student_id,))
        cur.execute("DELETE FROM students WHERE id = %s;", (student_id,))
        conn.commit()
        print(f"\n✅ Student with ID {student_id} deleted successfully.")
        cur.close()
    except Exception as error:
        print("❌ Error deleting student:", error)

def delete_comments(conn):
    try:
        comment_id = int(input("Enter the comment ID to delete: "))
        cur = conn.cursor()
        cur.execute("DELETE FROM notes_comments WHERE id = %s;", (comment_id,))
        conn.commit()
        print("🗒️ Comment deleted.")
        cur.close()
    except Exception as error:
        print("❌ Error deleting comment:", error)

def add_comments(conn):
    try:
        student_id = int(input("Enter student ID to add comment: "))
        comment = input("Enter your comment: ")
        cur = conn.cursor()
        cur.execute("INSERT INTO notes_comments (student_id, comment) VALUES (%s, %s);", (student_id, comment))
        conn.commit()
        print("✅ Comment added.")
        cur.close()
    except Exception as error:
        print("❌ Error adding comment:", error)

def print_grades_temp(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM grades_temp;")
    rows = cur.fetchall()
    print("\n📊 Temporary Grades Data (grades_temp):")
    print(f"{'Student ID':<10} | {'Subject':<10} | {'Grade':<5} | {'Validation Status'}")
    print("-" * 50)
    for row in rows:
        student_id, subject_name, grade, validation_status = row
        print(f"{student_id:<10} | {subject_name:<10} | {grade:<5} | {validation_status}")
    print("-" * 50)
    cur.close()


def menu():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Student/Grades",
            user="postgres",
            password="Emanueli1"
        )
        print("[DEBUG] Connected to Student Database.\n")

        while True:
            print("\nChoose an action:")
            print("1. View all students")
            print("2. Add a new student")
            print("3. Delete a student")
            print("4. View Comments")
            print("5. Delete Comments")
            print("6. Add Comments")
            print("7. View Subjects")
            print("8. Add Grade to Student")
            print("T. Temp Grade View")
            print("9. Exit")
            choice = input("Enter choice (1-9): ")

            if choice == "1":
                print_all_students(conn)
            elif choice == "2":
                add_student(conn)
            elif choice == "3":
                delete_student(conn)
            elif choice == "4":
                view_comments(conn)
            elif choice == "5":
                delete_comments(conn)
            elif choice == "6":
                add_comments(conn)
            elif choice == "7":
                view_subjects(conn)
            elif choice == "8":
                add_grade(conn)
            elif choice == "T":
                print_grades_temp(conn)
            elif choice == "9":
                print("👋 Exiting...")
                break
            else:
                print("Invalid choice. Please select 1-9.")

        conn.close()

    except Exception as e:
        print("❌ Could not connect to database:", e)

if __name__ == "__main__":
    menu()
