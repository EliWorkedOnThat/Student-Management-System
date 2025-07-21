import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
import psycopg2

def open_delete_note_window(parent):
    def delete_note():
        note_id = note_id_entry.get()
        if not note_id.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid numeric Note ID.")
            return

        try:
            conn = psycopg2.connect(
                host="your_host",
                database="your_db_name",
                user="your_username",
                password="your_passcode"
            )
            cur = conn.cursor()
            cur.execute("DELETE FROM notes_comments WHERE id = %s", (int(note_id),))
            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Success", f"Note ID {note_id} has been deleted.")
            print("Note deleted from note list ✅")
            popup.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"Could not delete note.. Error: {e}")

    # Popup window
    popup = Toplevel(parent)
    popup.title("Delete Note")
    popup.geometry("400x200")
    popup.resizable(True, True)

    # Frame inside popup
    frame = ttk.Frame(popup, padding=20)
    frame.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame, text="Enter Note ID to Delete:").pack(pady=(0, 10))
    note_id_entry = ttk.Entry(frame)
    note_id_entry.pack(pady=5, fill=tk.X)

    delete_button = ttk.Button(frame, text="Delete Note", command=delete_note)
    delete_button.pack(pady=20)
