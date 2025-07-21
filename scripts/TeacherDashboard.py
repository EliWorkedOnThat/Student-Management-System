import tkinter as tk
from tkinter import Toplevel, messagebox
import psycopg2
from AddStudent import add_student
from DataVisualization import show_grade_pie_chart
from DeleteStudent import delete_student
from ShowGrades import show_all_grades_popup
from Add_Delete_Grade import delete_grade_by_id , add_grade
from notes import pull_notes
from delete_note import open_delete_note_window
from add_note import open_add_note_window
from CONTACT import open_contact_student_window

def open_delete_grade_window(root):
    popup = Toplevel(root)
    popup.title("Delete Grade")
    popup.geometry("250x200")

    tk.Label(popup, text="Enter Grade ID to delete:").pack(pady=10)
    grade_id_entry = tk.Entry(popup)
    grade_id_entry.pack(pady=5)

    def submit_delete():
        try:
            grade_id = int(grade_id_entry.get())
            delete_grade_by_id(grade_id)
            messagebox.showinfo("Success", f"Grade ID {grade_id} deleted.")
            popup.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete grade: {e}")

    tk.Button(popup, text="Delete Grade", command=submit_delete).pack(pady=15)

def open_add_grade_window(root):
    popup = Toplevel(root)
    popup.title("Add Grade")
    popup.geometry("400x350")

    tk.Label(popup, text="Student ID:").pack(pady=5)
    student_entry = tk.Entry(popup)
    student_entry.pack()

    tk.Label(popup, text="Subject ID:").pack(pady=5)
    subject_entry = tk.Entry(popup)
    subject_entry.pack()

    tk.Label(popup, text="Grade (e.g., A/B+/F):").pack(pady=5)
    grade_entry = tk.Entry(popup)
    grade_entry.pack()

    def submit_add():
        try:
            student_id = int(student_entry.get())
            subject_id = int(subject_entry.get())
            grade = grade_entry.get().strip().upper()
            if not grade:
                raise ValueError("Grade cannot be empty.")
            add_grade(student_id, subject_id, grade)
            messagebox.showinfo("Success", "Grade added.")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(popup, text="Submit Grade", command=submit_add).pack(pady=20)


def open_delete_student_window(root, refresh_students_callback):
    popup = Toplevel(root)
    popup.title("Delete Student")
    popup.geometry("300x150")

    tk.Label(popup, text="Enter Student ID to delete:").pack(pady=5)
    id_entry = tk.Entry(popup, width=30)
    id_entry.pack(pady=5)

    def submit_delete():
        student_id_str = id_entry.get().strip()
        if not student_id_str.isdigit():
            messagebox.showerror("Invalid input", "Please enter a valid numeric ID.")
            return
        student_id = int(student_id_str)

        try:
            delete_student(student_id)
            messagebox.showinfo("Success", f"Student with ID {student_id} deleted.")
            popup.destroy()
            refresh_students_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")

    tk.Button(popup, text="Delete Student", command=submit_delete).pack(pady=10)

def open_add_student_window(root):
    popup = Toplevel(root)
    popup.title("Add Student")
    popup.geometry("400x350")

    tk.Label(popup, text="Student Name:").pack(pady=5)
    name_entry = tk.Entry(popup, width=50)
    name_entry.pack()

    tk.Label(popup, text="Email:").pack(pady=5)
    email_entry = tk.Entry(popup, width=50)
    email_entry.pack()

    tk.Label(popup, text="Class Number:").pack(pady=5)
    class_entry = tk.Entry(popup, width=50)
    class_entry.pack()

    tk.Label(popup, text="Overall Grade:").pack(pady=5)
    grade_entry = tk.Entry(popup, width=50)
    grade_entry.pack()

    def submit_student():
        name = name_entry.get().strip()
        class_number = class_entry.get().strip()
        email = email_entry.get().strip()
        overall_grade = grade_entry.get().strip()
        if name and email and class_number and overall_grade:
            try:
                add_student(name, email, class_number, overall_grade)
                popup.destroy()
                root.load_students()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add student: {e}")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    tk.Button(popup, text="Add Student", command=submit_student).pack(pady=15)

class TeacherDashboard(tk.Tk):
    def __init__(self, teacher_name, class_number):
        super().__init__()
        self.teacher_name = teacher_name
        self.class_number = class_number
        self.title(f"Dashboard - {teacher_name}")
        self.geometry("1000x1000")
        self.configure(bg="Grey")
        self.resizable(True , True)

        label = tk.Label(self, bg=self["bg"], font=("Arial", 20, "bold"),
                         text=f"Welcome to the dashboard, {teacher_name}!")
        label.pack(pady=20)

        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="Student/Grades",
                user="postgres",
                password="Emanueli1"
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            self.destroy()
            return

        self.students_frame = tk.Frame(self, bg=self["bg"])
        self.students_frame.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=20)

        self.load_students()

        button_frame = tk.Frame(self, bg="Grey")
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # --- Green Buttons: Add Actions ---
        add_student_button = tk.Button(
            button_frame, bg="lightgreen", width=10, height=3, text="Add Student",
            command=lambda: open_add_student_window(self)
        )
        add_student_button.pack(pady=10, fill=tk.X)

        add_grade_button = tk.Button(
            button_frame, bg="lightgreen", width=10, height=3, text="Add Grade",
            command=lambda: open_add_grade_window(self)
        )
        add_grade_button.pack(pady=10, fill=tk.X)

        add_note_button = tk.Button(
            button_frame, bg="lightgreen", width=10, height=3, text="Add Note",
            command=lambda: open_add_note_window(self)
        )
        add_note_button.pack(pady=10, fill=tk.X)

        delete_student_button = tk.Button(
            button_frame, bg="red", width=10, height=3, text="Delete Student",
            command=lambda: open_delete_student_window(self, self.load_students)
        )
        delete_student_button.pack(pady=10, fill=tk.X)

        delete_grade_button = tk.Button(
            button_frame, bg="red", width=10, height=3, text="Delete Grade",
            command=lambda: open_delete_grade_window(self)
        )
        delete_grade_button.pack(pady=10, fill=tk.X)

        delete_note_button = tk.Button(
            button_frame, bg="red", width=10, height=3, text="Delete Note",
            command=lambda: open_delete_note_window(self)
        )
        delete_note_button.pack(pady=10, fill=tk.X)

        view_grades_button = tk.Button(
            button_frame, bg="lightblue", width=10, height=3, text="View Grades",
            command=lambda: show_all_grades_popup(self, self.class_number)
        )
        view_grades_button.pack(pady=10, fill=tk.X)

        notes_button = tk.Button(
            button_frame, bg="lightblue", width=10, height=3, text="Show Notes",
            command=lambda: pull_notes(self, self.class_number)
        )
        notes_button.pack(pady=10, fill=tk.X)

        visualize_grades_button = tk.Button(
            button_frame, bg="lightblue", width=10, height=3, text="Grade Analysis",
            command=lambda: show_grade_pie_chart(self.class_number)
        )
        visualize_grades_button.pack(pady=10, fill=tk.X)

        contact_button = tk.Button(
            button_frame, bg="orange", width=10, height=3, text="Contact Student",
            command=lambda: open_contact_student_window(self, self.class_number)
        )
        contact_button.pack(pady=10, fill=tk.X)

    def load_students(self):
        for widget in self.students_frame.winfo_children():
            widget.destroy()

        try:
            self.cur.execute("""
                SELECT id, name FROM students
                WHERE class_number = %s
                ORDER BY name;
            """, (self.class_number,))
            students = self.cur.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch students: {e}")
            students = []

        for student_id, student_name in students:
            student_label = tk.Label(
                self.students_frame, text=f"{student_id}: {student_name}", font=("Arial", 12),
                bg="White", relief="groove", padx=10, pady=5
            )
            student_label.pack(fill=tk.X, pady=5)
