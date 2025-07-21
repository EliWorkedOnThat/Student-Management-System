import psycopg2

def print_grades():
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )

        cur = conn.cursor()

        cur.execute("SELECT id, student_id, subject_id, grade FROM grades ORDER BY id")
        rows = cur.fetchall()

        print("Grades Table:")
        print("-" * 60)
        for grade_id, student_id, subject_id, grade in rows:
            print(f"ID: {grade_id} | Student ID: {student_id} | Subject ID: {subject_id} | Grade: {grade}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Database error:", e)

def delete_grade_by_id(grade_id):
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()


        cur.execute(
            "DELETE FROM grades WHERE id = %s",
            (grade_id,)
        )
        conn.commit()
        print(f"Deleted grade with ID {grade_id}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Failed to delete grade:", e)

def add_grade(student_id, subject_id, grade):
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO grades (student_id, subject_id, grade, graded_on) VALUES (%s, %s, %s, NOW())",
            (student_id, subject_id, grade)
        )
        conn.commit()
        print(f"Added grade {grade} for Student ID {student_id}, Subject ID {subject_id}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Failed to add grade:", e)


