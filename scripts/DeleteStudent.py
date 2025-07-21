import psycopg2

def delete_student(student_id):
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()

        # Delete from grades and attendance first, then students
        cur.execute("DELETE FROM grades WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM attendance WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))

        conn.commit()
        print(f"✅ Student with id {student_id} and related records deleted.")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Failed to delete student:", e)
