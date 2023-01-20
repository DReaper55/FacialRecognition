import tkinter as tk
from tkinter import ttk

from database.student_db import getAllStudents, getOneStudent
from utils.display_student_info import displayStudentInfo
from utils.mongodb_constants import StudentDBConstants


def show_home_page(self):
    self.main_frame.destroy()
    self.main_frame = tk.Frame(self, bg='white')
    self.main_frame.pack(side='right', fill='both', expand=True)

    # Create the header
    label = tk.Label(self.main_frame, text="Attendance Management System", bg='white', font=("Helvetica", 24))
    label.pack()

    search_box_frame = tk.Frame(self.main_frame, bg='white')

    # Create the table title
    title = tk.Label(search_box_frame, text="Student Records", bg="white", font=("Helvetica", 14))
    title.grid(row=0, column=0, pady=10, sticky="w")

    # Create the search box
    search_box = ttk.Entry(search_box_frame)
    search_box.insert(0, "Search...")
    search_box.grid(row=0, column=1, padx=10, pady=10,ipadx=100, sticky="w")

    # Create the search button
    search_button = ttk.Button(search_box_frame, text="Search")
    search_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # Create the new student creation button
    search_button = ttk.Button(search_box_frame, text="New", command=lambda: displayStudentInfo(True)
                               )
    search_button.grid(row=0, column=3, padx=10, pady=30, sticky="e")

    search_box_frame.pack()

    # Create the table
    table = ttk.Treeview(self.main_frame, columns=(
        StudentDBConstants.FullName,
        StudentDBConstants.Faculty,
        StudentDBConstants.Department,
        StudentDBConstants.Matric,
        StudentDBConstants.Gender,
        StudentDBConstants.DateOfBirth,
    ), show="headings")
    table.pack(expand=True, fill='both')

    # Create the horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(self.main_frame, orient="horizontal", command=table.xview)
    x_scrollbar.pack(side='bottom', fill='x')

    # Create the vertical scrollbar
    y_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=table.yview)
    y_scrollbar.pack(side='right', fill='y')

    # Attach the scrollbar to the table
    table.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    # Bind the event handler function to the <<TreeviewSelect>> event
    table.bind("<<TreeviewOpen>>", lambda x: on_row_select(table))

    # Set the column headings
    table.heading(StudentDBConstants.FullName, text=StudentDBConstants.FullName)
    table.heading(StudentDBConstants.Faculty, text=StudentDBConstants.Faculty)
    table.heading(StudentDBConstants.Department, text=StudentDBConstants.Department)
    table.heading(StudentDBConstants.Matric, text=StudentDBConstants.Matric)
    table.heading(StudentDBConstants.Gender, text=StudentDBConstants.Gender)
    table.heading(StudentDBConstants.DateOfBirth, text=StudentDBConstants.DateOfBirth)

    # Insert some data into the table
    students = getAllStudents()
    for student in students:
        table.insert("", "end", values=(
            student.Fullname,
            student.Faculty,
            student.Department,
            student.Matric,
            student.Gender,
            student.DateOfBirth,
        ), iid=student.Matric, )


def on_row_select(table):
    selected_item = table.selection()

    # Get the matric number of the student in the selected row
    matricNumber = table.item(selected_item)['values'][3]

    student = getOneStudent(matricNumber)

    displayStudentInfo(False, student=student)
