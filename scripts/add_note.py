import tkinter as tk
import psycopg2
from tkinter import Toplevel, messagebox, ttk

def open_add_note_window(parent):
    def submit_note():
        student_id = student_id_entry.get().strip()
        comment = comment_entry.get("1.0", tk.END).strip()

        if not student_id.isdigit() or not comment:
            messagebox.showwarning("Invalid Input", "Please enter a valid student ID and a non-empty comment.")
            return

        try:
            conn = psycopg2.connect(
                host="your_host",
                database="your_db_name",
                user="your_username",
                password="your_passcode"
            )
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO notes_comments (student_id, comment) VALUES (%s, %s)",
                (int(student_id), comment)
            )
            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Success", "Note added successfully.")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    popup = Toplevel(parent)
    popup.title("Add Note/Comment")
    popup.geometry("600x400")
    popup.resizable(True, True)

    frame = ttk.Frame(popup, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Student ID:").pack(anchor="w", pady=(0, 5))
    student_id_entry = ttk.Entry(frame)
    student_id_entry.pack(fill=tk.X, pady=(0, 15))

    ttk.Label(frame, text="Note / Comment:").pack(anchor="w", pady=(0, 5))
    comment_entry = tk.Text(frame, height=10, wrap="word")
    comment_entry.pack(fill=tk.BOTH, expand=True)

    submit_button = ttk.Button(frame, text="Add Note", command=submit_note)
    submit_button.pack(pady=15)

