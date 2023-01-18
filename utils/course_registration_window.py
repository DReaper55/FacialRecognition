import tkinter as tk
from tkinter import ttk

from database.registered_students_db import getOneRegisteredStudent, insert, delete
from database.student_db import getAllStudents, getOneStudent
from model.registered_student import RegisteredStudent
from utils.display_student_info import displayStudentInfo
from utils.mongodb_constants import StudentDBConstants


def show_registration_window(course, isRegister):
    root = tk.Tk()
    root.title("Course Registration")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.configure(bg='#f0f0f0')

    # Create the header
    label = tk.Label(root, text=f"{course.courseTitle} Registration", font=("Helvetica", 24))
    label.pack()

    search_box_frame = tk.Frame(root)

    if isRegister:
        tableTitleText = "Unregistered Students"
    else:
        tableTitleText = "Registered Students"

    # Create the table title
    title = tk.Label(search_box_frame, text=tableTitleText, font=("Helvetica", 14))
    title.grid(row=0, column=0, pady=10, sticky="w")

    # Create the search box
    search_box = ttk.Entry(search_box_frame)
    search_box.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Create the search button
    search_button = ttk.Button(search_box_frame, text="Search")
    search_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    search_box_frame.pack()

    # Create the table
    table = ttk.Treeview(root, columns=(
        StudentDBConstants.FullName,
        StudentDBConstants.Faculty,
        StudentDBConstants.Department,
        StudentDBConstants.Matric,
        StudentDBConstants.Gender,
        StudentDBConstants.DateOfBirth,
    ), show="headings")
    table.pack(expand=True, fill='both')

    # Create the horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=table.xview)
    x_scrollbar.pack(side='bottom', fill='x')

    # Create the vertical scrollbar
    y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    y_scrollbar.pack(side='right', fill='y')

    # Attach the scrollbar to the table
    table.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    # Bind the event handler function to the <<TreeviewSelect>> event
    table.bind("<<TreeviewOpen>>", lambda x: on_row_select(table, course, isRegister))

    # Set the column headings
    table.heading(StudentDBConstants.FullName, text=StudentDBConstants.FullName)
    table.heading(StudentDBConstants.Faculty, text=StudentDBConstants.Faculty)
    table.heading(StudentDBConstants.Department, text=StudentDBConstants.Department)
    table.heading(StudentDBConstants.Matric, text=StudentDBConstants.Matric)
    table.heading(StudentDBConstants.Gender, text=StudentDBConstants.Gender)
    table.heading(StudentDBConstants.DateOfBirth, text=StudentDBConstants.DateOfBirth)

    # Get registered students
    regStudents = getOneRegisteredStudent(course.courseCode)

    # Insert some data into the table

    if isRegister:
        students = getAllStudents()
        for student in students:
            # Using list comprehension to find registered
            result = [regStudent for regStudent in regStudents if regStudent.studentMatric == student.Matric]

            # Add student to table
            if not result:
                table.insert("", "end", values=(
                    student.Fullname,
                    student.Faculty,
                    student.Department,
                    student.Matric,
                    student.Gender,
                    student.DateOfBirth,
                ), iid=student.Matric, )

    if not isRegister:
        # Add registered students from studentsDb to table
        for regStudent in regStudents:
            student = getOneStudent(regStudent.studentMatric)

            table.insert("", "end", values=(
                student.Fullname,
                student.Faculty,
                student.Department,
                student.Matric,
                student.Gender,
                student.DateOfBirth,
            ), iid=student.Matric, )


def on_row_select(table, course, isRegister):
    selected_item = table.selection()

    # Get the matric number of the student in the selected row
    matricNumber = table.item(selected_item)['values'][3]

    #     Add student to registered database
    if isRegister:
        insert(RegisteredStudent(
            courseCode=course.courseCode,
            studentMatric=matricNumber,
        ))
    else:
        delete(matricNumber)

        # todo: add a notification

    # remove item  from table after registering student
    table.delete(selected_item)
