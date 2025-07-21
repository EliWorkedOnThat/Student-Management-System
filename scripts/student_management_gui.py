import tkinter as tk
from tkinter import messagebox
from TeacherDashboard import TeacherDashboard
from DataVisualization import show_grade_pie_chart

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Teacher Login")
        self.geometry("465x400")
        self.resizable(False, False)
        self.configure(bg="Light Blue")

        self.valid_users = {
            "Teacher1": "12B",
            "Teacher2": "11C"
        }

        label_font = ("Arial", 12)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")

        Welcome_Message = tk.Label(
            self,
            text="Welcome to Teacher Student Management Panel",
            font=("Arial", 14, "bold"),
            bg=self["bg"]
        )
        Welcome_Message.pack(pady=(20, 10))

        tk.Label(self, text="Username:", bg=self["bg"], font=label_font).pack(pady=(10, 2))
        self.username_entry = tk.Entry(self, font=entry_font, width=28)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg=self["bg"], font=label_font).pack(pady=(10, 2))
        self.password_entry = tk.Entry(self, show="*", font=entry_font, width=28)
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", font=button_font, width=20, height=2, command=self.check_login).pack(pady=15)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both fields")
            return

        if username in self.valid_users and self.valid_users[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.destroy()

            dashboard = TeacherDashboard(username, password)
            dashboard.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
