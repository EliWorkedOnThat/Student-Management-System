import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
import psycopg2

def show_all_grades_popup(parent, class_number):
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT g.id, s.name AS student_name, sub.name AS subject_name, g.grade, g.graded_on
            FROM grades g
            JOIN students s ON g.student_id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            WHERE s.class_number = %s
            ORDER BY g.id;
        """, (class_number,))
        results = cur.fetchall()
        cur.close()
        conn.close()

        popup = Toplevel(parent)
        popup.title(f"Grades for Class {class_number}")
        popup.geometry("600x400")
        popup.resizable(True, True)

        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_box = tk.Text(frame, yscrollcommand=scrollbar.set, wrap="none")
        text_box.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_box.yview)

        for row in results:
            line = f"Grade ID: {row[0]}, Student: {row[1]}, Subject: {row[2]}, Grade: {row[3]}, Date: {row[4]}\n"
            text_box.insert(tk.END, line)

        text_box.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load grades:\n{e}")
