import tkinter as tk
from tkinter import ttk , Toplevel , messagebox
import webbrowser
import psycopg2

def open_contact_student_window(root, class_number):
    popup = Toplevel(root)
    popup.title("Contact a Student")
    popup.geometry("450x250")

    tk.Label(popup, text="Select student email to contact:", font=("Arial", 12)).pack(pady=15)

    email_var = tk.StringVar()
    email_dropdown = ttk.Combobox(popup, textvariable=email_var, state="readonly", width=40, font=("Arial", 12))
    email_dropdown.pack(pady=10)

    try:
        conn = psycopg2.connect(
            host="your_host",
            database="your_db_name",
            user="your_username",
            password="your_passcode"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT email FROM students WHERE class_number = %s AND email IS NOT NULL ORDER BY email;
        """, (class_number,))
        emails = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        email_dropdown["values"] = emails
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not load emails: {e}")
        popup.destroy()
        return

    def contact_student():
        selected_email = email_var.get()
        if selected_email:
            gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={selected_email}"
            webbrowser.open(gmail_url)
        else:
            messagebox.showwarning("No Selection", "Please select an email.")

    contact_btn = tk.Button(popup, text="Contact", font=("Arial", 12, "bold"), width=20, height=2, command=contact_student)
    contact_btn.pack(pady=20)
