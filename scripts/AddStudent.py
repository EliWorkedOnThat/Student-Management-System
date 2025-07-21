import psycopg2

def add_student(name, email, class_number, overall_grade):
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()
        query = """
            INSERT INTO students (name, email, class_number, overall_grade)
            VALUES (%s, %s, %s, %s);
        """
        cur.execute(query, (name, email, class_number, overall_grade))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Successfully added student: {name}")
    except psycopg2.Error as e:
        print("❌ Database error:", e)
