import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
import psycopg2

def pull_notes(parent, class_number):
    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()
        query = """
            SELECT n.id, n.student_id, n.comment, n.created_on
            FROM notes_comments n
            JOIN students s ON n.student_id = s.id
            WHERE s.class_number = %s
            ORDER BY n.created_on DESC;
        """
        cur.execute(query, (class_number,))
        results = cur.fetchall()
        cur.close()
        conn.close()

        popup = Toplevel(parent)
        popup.title("Student Notes and Comments")
        popup.geometry("600x400")
        popup.resizable(True, True)

        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_box = tk.Text(frame, yscrollcommand=scrollbar.set, wrap="word")
        text_box.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_box.yview)

        for note in results:
            line = f"Note ID: {note[0]}, Student ID: {note[1]}, Note: {note[2]}, Date: {note[3]}\n"
            text_box.insert(tk.END, line)

        text_box.config(state=tk.DISABLED)

    except Exception as e:
        print(f"An error with fetching notes...: {e}")
