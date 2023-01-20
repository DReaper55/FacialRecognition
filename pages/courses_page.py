import tkinter as tk
from tkinter import ttk

from database.courses_db import getAllCourses, getOneCourse
from utils.display_course_info import displayCourseInfo
from utils.mongodb_constants import CoursesDBConstants


def show_courses_page(self):
    self.main_frame.destroy()
    self.main_frame = tk.Frame(self, bg='white')
    self.main_frame.pack(side='right', fill='both', expand=True)

    # Create the header
    label = tk.Label(self.main_frame, text="Attendance Management System", bg='white', font=("Helvetica", 24))
    label.pack()

    search_box_frame = tk.Frame(self.main_frame, bg='white')

    # Create the table title
    title = tk.Label(search_box_frame, text="Courses", bg="white", font=("Helvetica", 14))
    title.grid(row=0, column=0, pady=10, sticky="w")

    # Create the search box
    search_box = ttk.Entry(search_box_frame)
    search_box.insert(0, "Search...")
    search_box.grid(row=0, column=1, padx=10, pady=10, ipadx=100, sticky="w")

    # Create the search button
    search_button = ttk.Button(search_box_frame, text="Search")
    search_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # Create the new course creation button
    search_button = ttk.Button(search_box_frame, text="New", command=lambda: displayCourseInfo(True)
                               )
    search_button.grid(row=0, column=3, padx=10, pady=30, sticky="e")

    search_box_frame.pack()

    # Create the table
    table = ttk.Treeview(self.main_frame, columns=(
        CoursesDBConstants.courseCode,
        CoursesDBConstants.courseTitle,
        CoursesDBConstants.courseLecturer,
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
    table.heading(CoursesDBConstants.courseCode, text="Course Code")
    table.heading(CoursesDBConstants.courseTitle, text="Course Title")
    table.heading(CoursesDBConstants.courseLecturer, text="Course Lecturer")

    # Insert some data into the table
    courses = getAllCourses()
    for course in courses:
        table.insert("", "end", values=(
            course.courseCode,
            course.courseTitle,
            course.courseLecturer,
        ), iid=course.courseCode, )


def on_row_select(table):
    selected_item = table.selection()

    # Get the matric number of the course in the selected row
    courseCode = table.item(selected_item)['values'][0]

    course = getOneCourse(courseCode)

    displayCourseInfo(False, course)
