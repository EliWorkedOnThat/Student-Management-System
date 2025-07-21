Student Management System
This is a desktop-based Student Management System built using Python and PostgreSQL.

Python handles the core logic and GUI of the application through Tkinter, while PostgreSQL—along with the included sample CSV file—is used for data storage and management.

🚀 Features
Add, update, and delete student records

View grades in a scrollable popup

Add and delete grades

Add, delete, and view student notes

Visualize grades using a pie chart with percentage labels

Store data securely in a PostgreSQL database

Contact students via email using a built-in browser launcher

Sample .csv file for testing student data

Clean and responsive Tkinter GUI

And more...

🛠 Setup Instructions
Make sure you have Python and PostgreSQL installed on your system.

1. Install the required Python libraries
bash
Copy
Edit
pip install psycopg2
pip install tkinter
pip install matplotlib
Note: On some systems, tkinter might already be installed. If you face issues, look up how to install Tkinter based on your OS (e.g., sudo apt install python3-tk for Ubuntu).

2. Set Up the Database
Open pgAdmin or your preferred PostgreSQL tool.

Create a new database (e.g., student_db).

Run the provided .sql file to create the necessary tables and structure.

3. Configure the Database Connection

In each Python script, locate the database connection block:

python
Copy
Edit
host = "your_host",
database = "your_db_name",
user = "your_username",
password = "your_passcode"

Replace the values with your actual PostgreSQL credentials.

##NOTE the .CSV file is used only as an option if you want to scale the application so no functionalities were placed for it outside of the Database file itself...
