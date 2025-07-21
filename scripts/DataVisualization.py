import psycopg2
from collections import Counter
import matplotlib.pyplot as plt


def show_grade_pie_chart(class_number):
    color_map = {
        'A': '#4CAF50',  # Green
        'B': '#32CD32',  # Lime Green
        'C': '#FFFF00',  # Yellow
        'D': '#FF5722',  # Deep Orange
        'F': '#FF0000'  # Red
    }

    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()

        # Filter grades only for students in the specified class
        cur.execute("""
            SELECT g.grade
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE s.class_number = %s
        """, (class_number,))

        grades = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()

        if not grades:
            print(f"No grades found for class {class_number}.")
            return

        grade_counts = Counter(grades)
        labels = grade_counts.keys()
        sizes = grade_counts.values()

        plt.figure(figsize=(6, 6))
        plt.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=[color_map.get(grade, '#808080') for grade in labels]  # default gray for unknown
        )
        plt.title(f"Grade Frequency in Class {class_number}")
        plt.axis("equal")
        plt.show()

    except Exception as e:
        print("Error generating grade chart:", e)
